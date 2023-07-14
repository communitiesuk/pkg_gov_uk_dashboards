/**
 * @type {HTMLElement | null | undefined}
 */
var mobileNav = null;
/**
 * @type {boolean}
 */
var isOpen = false;
 
if (typeof attachEventToDash !== 'undefined') {
    attachEventToDash('mobile-menu-btn', 'click', function () {
        if (mobileNav === null) {
            mobileNav = document.getElementById('nav-section')
            if (!mobileNav) {
                return;
            }
        }
        mobileNav.style.display = isOpen ? 'none' : 'inline-block';
        isOpen = !isOpen;
    }, false)

// attach click events that close the menu to links in the nav menu 
var numberOfLinks = 8; // ideally get dynamically but document.querySelectorAll and trying to match id before attaching event to Dash didn't work.. 
for (var i = 0; i < numberOfLinks; i++) {
    var linkId = 'nav-bar-link-' + i + '-mobile';
    attachEventToDash(linkId, 'click', function () {
        if (mobileNav === null) {
            mobileNav = document.getElementById('nav-section')
            if (!mobileNav) {
                return;
            }
        }
        mobileNav.style.display = 'none';
        isOpen = false;
        }, false);
}

/**
 *
 * @param {function} func
 * @param {number} time
 * @returns
 */
function debounce(func, time) {
    var time = time || 100; // 100 by default if no param
    var timer;
    return function (event) {
        if (timer) clearTimeout(timer);
        timer = setTimeout(func, time, event);
    };
}

window.addEventListener(
    "resize",
    debounce(function () {
        if (mobileNav) {
            var mq = window.matchMedia("(min-width: 992px)");
            if (mq.matches) {
                isOpen = false;
                mobileNav.style.display = 'none';
            }
        }
    }, 150)
);}