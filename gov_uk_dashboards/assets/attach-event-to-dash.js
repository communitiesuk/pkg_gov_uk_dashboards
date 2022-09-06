/**
 *
 * @param {string} id
 * @param {*} event
 * @param {(this: HTMLElement, ev: any) => any} callback
 * @param {boolean | AddEventListenerOptions} options
 */
function attachEventToDash(id, event, callback, options) {
	var observer = new MutationObserver(function (_mutations, obs) {
		var ele = document.getElementById(id);
		if (ele) {
			ele.addEventListener(event, callback, options);
			obs.disconnect();
		}
	});
	window.addEventListener('DOMContentLoaded', function () {
		observer.observe(document, {
			childList: true,
			subtree: true
		});
	})
}