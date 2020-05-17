

$(function ($) {
    $.fn.timedHover = function (fnOver, fnOut, options) {
        let settings = $.extend({
            hoverTimeout: 150,
            leavingTimeout: 300,
        }, options);

        this.hover(function (event) {
            let el = $(this);
            let leavingTimeout = el.data("hover-leaving-timeout");
            if (leavingTimeout) {
                clearTimeout(leavingTimeout);
                el.removeData("hover-leaving-timeout");
            } else {
                el.data("hover-entering-timeout", setTimeout(function () {
                    fnOver(event);
                    el.removeData("hover-entering-timeout");
                }, settings.hoverTimeout));
            }
        }, function (event) {
            let el = $(this);
            let enteringTimeout = el.data("hover-entering-timeout");
            if (enteringTimeout) {
                clearTimeout(enteringTimeout);
                el.removeData("hover-entering-timeout");
            } else {
                el.data("hover-leaving-timeout", setTimeout(function () {
                    fnOut(event);
                    el.removeData("hover-leaving-timeout");
                }, settings.leavingTimeout));
            }
        });
    }
}(jQuery));
