import json
import csv
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum, Avg
from django.core.paginator import Paginator
from django.http import HttpResponse
from datetime import datetime
from .models import SatelliteErrorLog


def home(request):
	return render(request, 'ventures/home.html')


@login_required
def satellites_dashboard(request):
	"""Dashboard de logs de errores de satélites WayneTech."""
	total_logs = SatelliteErrorLog.objects.count()
	
	if total_logs == 0:
		return render(request, 'ventures/satellites_dashboard.html', {'sin_datos': True})
	
	# Estadísticas generales
	critical_count = SatelliteErrorLog.objects.filter(severity='CRITICAL').count()
	unresolved = SatelliteErrorLog.objects.filter(resolved=False).count()
	requires_action = SatelliteErrorLog.objects.filter(requires_action=True).count()
	unique_satellites = SatelliteErrorLog.objects.values('satellite_id').distinct().count()
	
	# Por severidad
	by_severity = (
		SatelliteErrorLog.objects
		.values('severity')
		.annotate(count=Count('id'))
		.order_by('-count')
	)
	
	# Por tipo de satélite
	by_sat_type = (
		SatelliteErrorLog.objects
		.values('satellite_type')
		.annotate(count=Count('id'))
		.order_by('-count')
	)
	
	# Por código de error (top 10)
	by_error_code = (
		SatelliteErrorLog.objects
		.values('error_code', 'error_description')
		.annotate(count=Count('id'))
		.order_by('-count')[:10]
	)
	
	# Por satélite (más activos)
	by_satellite = (
		SatelliteErrorLog.objects
		.values('satellite_id', 'satellite_name')
		.annotate(count=Count('id'))
		.order_by('-count')[:10]
	)
	
	# Por subsistema
	by_subsystem = (
		SatelliteErrorLog.objects
		.values('subsystem')
		.annotate(count=Count('id'))
		.order_by('-count')[:8]
	)
	
	# Status de resolución
	resolved_count = SatelliteErrorLog.objects.filter(resolved=True).count()
	
	def qs_to_json(qs, label, value):
		return json.dumps([{label: str(r[label] or ''), value: float(r[value] or 0)} for r in qs])
	
	context = {
		'total_logs': total_logs,
		'critical': critical_count,
		'unresolved': unresolved,
		'requires_action': requires_action,
		'unique_satellites': unique_satellites,
		'resolved': resolved_count,
		'critical_pct': round(critical_count / total_logs * 100, 1) if total_logs > 0 else 0,
		'resolved_pct': round(resolved_count / total_logs * 100, 1) if total_logs > 0 else 0,
		'by_severity_json': qs_to_json(by_severity, 'severity', 'count'),
		'by_sat_type_json': qs_to_json(by_sat_type, 'satellite_type', 'count'),
		'by_error_code_json': qs_to_json(by_error_code, 'error_code', 'count'),
		'by_satellite_json': qs_to_json(by_satellite, 'satellite_name', 'count'),
		'by_subsystem_json': qs_to_json(by_subsystem, 'subsystem', 'count'),
	}
	
	return render(request, 'ventures/satellites_dashboard.html', context)


@login_required
def satellites_list(request):
	"""Lista paginada de logs de errores."""
	logs = SatelliteErrorLog.objects.all().order_by('-timestamp')
	
	# Filtros opcionales
	severity_filter = request.GET.get('severity')
	satellite_filter = request.GET.get('satellite')
	resolved_filter = request.GET.get('resolved')
	critical_filter = request.GET.get('critical')
	subsystem_filter = request.GET.get('subsystem')
	date_from = request.GET.get('date_from')
	date_to = request.GET.get('date_to')
	search_query = request.GET.get('search', '')
	
	if severity_filter:
		logs = logs.filter(severity=severity_filter)
	if satellite_filter:
		logs = logs.filter(satellite_id=satellite_filter)
	if resolved_filter == 'true':
		logs = logs.filter(resolved=True)
	elif resolved_filter == 'false':
		logs = logs.filter(resolved=False)
	if critical_filter == 'true':
		logs = logs.filter(Q(severity='CRITICAL') | Q(requires_action=True))
	if subsystem_filter:
		logs = logs.filter(subsystem=subsystem_filter)
	if date_from:
		try:
			date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
			logs = logs.filter(timestamp__date__gte=date_from_obj.date())
		except ValueError:
			pass
	if date_to:
		try:
			date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
			logs = logs.filter(timestamp__date__lte=date_to_obj.date())
		except ValueError:
			pass
	if search_query:
		logs = logs.filter(
			Q(log_id__icontains=search_query) |
			Q(satellite_name__icontains=search_query) |
			Q(error_code__icontains=search_query) |
			Q(error_description__icontains=search_query) |
			Q(subsystem__icontains=search_query)
		)
	
	# Paginación
	paginator = Paginator(logs, 30)
	page_num = request.GET.get('page', 1)
	page_obj = paginator.get_page(page_num)
	
	# Opciones para filtros (deduplicadas y ordenadas)
	severities = SatelliteErrorLog.objects.values_list('severity', flat=True).distinct().order_by('severity')
	satellites = SatelliteErrorLog.objects.values('satellite_id', 'satellite_name').distinct().order_by('satellite_name')
	subsystems = SatelliteErrorLog.objects.values_list('subsystem', flat=True).distinct().order_by('subsystem')
	
	# Estadísticas de severidad
	from django.db.models import Count
	severity_stats = (
		SatelliteErrorLog.objects
		.values('severity')
		.annotate(count=Count('severity'))
		.order_by('-count')
	)
	
	# Logs únicos por satélite (sin repetir)
	unique_satellites_count = SatelliteErrorLog.objects.values('satellite_id').distinct().count()
	
	context = {
		'page_obj': page_obj,
		'severities': severities,
		'satellites': satellites,
		'subsystems': subsystems,
		'current_severity': severity_filter,
		'current_satellite': satellite_filter,
		'current_resolved': resolved_filter,
		'current_critical': critical_filter,
		'current_subsystem': subsystem_filter,
		'current_date_from': date_from,
		'current_date_to': date_to,
		'current_search': search_query,
		'severity_stats': severity_stats,
		'unique_satellites_count': unique_satellites_count,
		'total_logs': logs.count(),
	}
	
	return render(request, 'ventures/satellites_list.html', context)


@login_required
def satellite_detail(request, log_id):
	"""Detalle de un log de error específico."""
	log = get_object_or_404(SatelliteErrorLog, log_id=log_id)
	
	# Logs relacionados del mismo satélite
	related_logs = (
		SatelliteErrorLog.objects
		.filter(satellite_id=log.satellite_id)
		.exclude(log_id=log_id)
		.order_by('-timestamp')[:10]
	)
	
	context = {
		'log': log,
		'related_logs': related_logs,
		'is_critical': log.is_critical,
	}
	
	return render(request, 'ventures/satellite_detail.html', context)


@login_required
def export_csv(request):
	"""Exporta logs de satélites filtrados a CSV."""
	response = HttpResponse(content_type='text/csv; charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename="satellite_error_logs.csv"'
	response.write('\ufeff')  # BOM para Excel
	
	logs = SatelliteErrorLog.objects.all().order_by('-timestamp')
	
	# Aplicar los mismos filtros que en la lista
	if request.GET.get('severity'):
		logs = logs.filter(severity=request.GET['severity'])
	if request.GET.get('satellite'):
		logs = logs.filter(satellite_id=request.GET['satellite'])
	if request.GET.get('resolved') == 'true':
		logs = logs.filter(resolved=True)
	elif request.GET.get('resolved') == 'false':
		logs = logs.filter(resolved=False)
	if request.GET.get('subsystem'):
		logs = logs.filter(subsystem=request.GET['subsystem'])
	if request.GET.get('search'):
		search = request.GET['search']
		logs = logs.filter(
			Q(log_id__icontains=search) |
			Q(satellite_name__icontains=search) |
			Q(error_code__icontains=search) |
			Q(error_description__icontains=search) |
			Q(subsystem__icontains=search)
		)
	
	writer = csv.writer(response)
	writer.writerow([
		'Log ID', 'Fecha/Hora', 'Satélite', 'Error Code', 'Descripción Error',
		'Severidad', 'Subsistema', 'Estado', 'Requiere Acción', 'Resolución'
	])
	
	for log in logs:
		writer.writerow([
			log.log_id,
			log.timestamp.strftime('%d/%m/%Y %H:%M'),
			log.satellite_name,
			log.error_code,
			log.error_description,
			log.severity,
			log.subsystem,
			'Resuelto' if log.resolved else 'Pendiente',
			'Sí' if log.requires_action else 'No',
			log.resolution_action or 'N/A'
		])
	
	return response

