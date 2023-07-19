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

// Wait until the 'mobile-navigation-items' element is loaded
var checkExist = setInterval(function() {
    var element = document.getElementById('mobile-navigation-items');
    if (element) {
        clearInterval(checkExist);
        var links = element.getElementsByTagName('a');
        attachEventsToLinks(links);
    }
}, 100);

function attachEventsToLinks(links) {
    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        link.addEventListener('click', function() {
            var mobileNav =document.getElementById('nav-section');
            if (mobileNav) {
                mobileNav.style.display = 'none';
                isOpen = false;
            }
        }, false);
    }
}

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