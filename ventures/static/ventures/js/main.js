document.addEventListener('DOMContentLoaded', () => {
	const burger = document.querySelector('[data-ventures-burger]');
	const nav = document.querySelector('[data-ventures-nav]');

	if (burger && nav) {
		burger.addEventListener('click', () => {
			const isOpen = nav.classList.toggle('is-open');
			burger.setAttribute('aria-expanded', String(isOpen));
		});
	}
});
