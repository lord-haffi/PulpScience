"use strict";

$(function ($) {

    // Only count HTML whitespace
    // Other whitespace should count in values
    // https://infra.spec.whatwg.org/#ascii-whitespac
    // (copied from jQuery source)
    const classRegex = /[^\x20\t\r\n\f]+/g;
    const dropdownStyles = {
        ver: {
            top: "dropdown-top",
            bottom: "dropdown-bottom",
        },
        hor: {
            left: "dropdown-left",
            center: "dropdown-center",
            right: "dropdown-right",
        }
    };

    function alignSpecDefaults (el) {
        let classes = el.attr("class");
        let classList = classes ? classes.match(classRegex) : [];

        let specDefaults = {};
        for (let key in dropdownStyles.ver) {
            let index = classList.indexOf(dropdownStyles.ver[key]);
            if (index !== -1) {
                classList.splice(index, 1);
                specDefaults.ver = key;
                break;
            }
        }
        for (let key in dropdownStyles.hor) {
            let index = classList.indexOf(dropdownStyles.hor[key]);
            if (index !== -1) {
                classList.splice(index, 1);
                specDefaults.hor = key;
                break;
            }
        }
        el.attr("class", classList.join(" "));
        return specDefaults;
    }
    $.fn.hasCss = function (property, value) {
        let i = 0;
        let cur;
        while (cur = $(this[i++]))
            if (cur.css(property) === value)
                return true;
        return false;
    };

    $.fn.dropdownSetup = function (options) {

        let settings = $.extend({
            elementOffset: 23,
            windowPadding: 5,

            hoverTimeout: 150,
            leavingTimeout: 300,
            fadeInTime: 300,

            realign: true,
            defaults: {hor: "center", ver: "bottom"},
            priorElDefaults: true,

            dropdownClass: "dropdown-root",
            reposition: true,

            triggerHover: true,
            triggerClick: true
        }, options);

        return this.each(function () {
            let menu = $("> .dropdown-menu", this).clone();
            let menuContainer = $("<div></div>").append(menu);
            let dropButton = $(this);
            let body = $("body");

            menuContainer.addClass(settings.dropdownClass);
            body.append(menuContainer);
            //dropButton.data("dropdown-menu", menu);
            dropButton.data("dropdown-container", menuContainer);

            dropButton.data("dropdown-settings", settings);
            if (settings.priorElDefaults)
                dropButton.data("dropdown-element-defaults", $.extend(settings.defaults, alignSpecDefaults(dropButton)));
            else
                dropButton.data("dropdown-element-defaults", settings.defaults);

            if (!settings.reposition)
                dropButton.dropdown("position");

            if (dropButton.css("position") === "fixed" ||
                dropButton.parents().hasCss("position", "fixed")) {

                dropButton.data("dropdown-is-fixed", true);
                menuContainer.css("position", "fixed");
            }


            if (settings.triggerClick) {
                body.on("click touch", function () {
                    dropButton.dropdown("hide");
                });
                dropButton.on("click touch", function (event) {
                    event.stopPropagation();
                    if (dropButton.dropdown("hidden"))
                        dropButton.dropdown("show");
                    else
                        dropButton.dropdown("hide");
                });
                menu.on("click touch", function (event) {
                    event.stopPropagation();
                });
            }

            if (settings.triggerHover) {

                // dropButton.hover(function () {
                //     // console.log("Entered dropButton.fnOver: ");
                //     // console.log("\tEntering Timeout: " + dropButton.data("dropdown-entering-timeout"));
                //     // console.log("\tLeaving Timeout: " + dropButton.data("dropdown-leaving-timeout"));
                //     let leavingTimeout = dropButton.data("dropdown-leaving-timeout");
                //     if (leavingTimeout) {
                //         clearTimeout(leavingTimeout);
                //         dropButton.removeData("dropdown-leaving-timeout");
                //     } else {
                //         dropButton.data("dropdown-entering-timeout", setTimeout(function () {
                //             dropButton.dropdown("show");
                //         }, settings.hoverTimeout));
                //     }
                // }, function () {
                //     // console.log("Entered dropButton.fnOut: ");
                //     // console.log("\tEntering Timeout: " + dropButton.data("dropdown-entering-timeout"));
                //     // console.log("\tLeaving Timeout: " + dropButton.data("dropdown-leaving-timeout"));
                //     let enteringTimeout = dropButton.data("dropdown-entering-timeout");
                //     if (enteringTimeout) {
                //         clearTimeout(enteringTimeout);
                //         dropButton.removeData("dropdown-entering-timeout");
                //     } else {
                //         dropButton.data("dropdown-leaving-timeout", setTimeout(function () {
                //             dropButton.dropdown("hide");
                //         }, settings.leavingTimeout));
                //     }
                // });
                dropButton.timedHover(function () {
                    dropButton.dropdown("show");
                }, function () {
                    dropButton.dropdown("hide");
                }, { leavingTimeout: settings.leavingTimeout, hoverTimeout: settings.hoverTimeout });
                menu.hover(function () {
                    // console.log("Entered menu.fnOver: ");
                    // console.log("\tEntering Timeout: " + dropButton.data("dropdown-entering-timeout"));
                    // console.log("\tLeaving Timeout: " + dropButton.data("dropdown-leaving-timeout"));
                    let leavingTimeout = dropButton.data("hover-leaving-timeout");
                    if (leavingTimeout) {
                        clearTimeout(leavingTimeout);
                        dropButton.removeData("hover-leaving-timeout");
                    }
                }, function () {
                    // console.log("Entered menu.fnOut: ");
                    // console.log("\tEntering Timeout: " + dropButton.data("dropdown-entering-timeout"));
                    // console.log("\tLeaving Timeout: " + dropButton.data("dropdown-leaving-timeout"));
                    dropButton.data("hover-leaving-timeout", setTimeout(function () {
                        dropButton.dropdown("hide");
                    }, settings.leavingTimeout));
                });
            }
        });
    };

    $.fn.dropdown = function (action) {
        switch (action) {
            case "show":
                this.each(function () {
                    let settings = $(this).data("dropdown-settings");
                    if (settings.triggerHover) {
                        // console.log("Entered show: ");
                        // console.log("\tEntering Timeout: " + $(this).data("dropdown-entering-timeout"));
                        // console.log("\tLeaving Timeout: " + $(this).data("dropdown-leaving-timeout"));
                        let enteringTimeout = $(this).data("hover-entering-timeout");
                        if (enteringTimeout) {
                            clearTimeout(enteringTimeout);
                            $(this).removeData("hover-entering-timeout");
                        }
                        let leavingTimeout = $(this).data("hover-leaving-timeout");
                        if (leavingTimeout) {
                            clearTimeout(leavingTimeout);
                            $(this).removeData("hover-leaving-timeout");
                        }
                    }
                    $(this).data("dropdown-container").fadeIn(settings.fadeInTime);
                    if (settings.reposition)
                        $(this).dropdown("position");
                });
                break;
            case "hide":
                this.each(function () {
                    if ($(this).data("dropdown-settings").triggerHover) {
                        // console.log("Entered hide: ");
                        // console.log("\tEntering Timeout: " + $(this).data("dropdown-entering-timeout"));
                        // console.log("\tLeaving Timeout: " + $(this).data("dropdown-leaving-timeout"));
                        let leavingTimeout = $(this).data("hover-leaving-timeout");
                        if (leavingTimeout) {
                            clearTimeout(leavingTimeout);
                            $(this).removeData("hover-leaving-timeout");
                        }
                    }
                    $(this).data("dropdown-container").hide();
                });
                break;
            case "position":
                this.each(function () {
                    let dropButton = $(this);
                    let dropdownPositioner = $(" .dropdown-positioner", this);
                    if (!dropdownPositioner)
                        dropdownPositioner = dropButton;
                    let menuContainer = dropButton.data("dropdown-container");
                    let menu = $("> .dropdown-menu", menuContainer);
                    let settings = dropButton.data("dropdown-settings");
                    let elDefaults = dropButton.data("dropdown-element-defaults");
                    let screenWidth = $(window).width(), screenHeight = $(window).height();
                    let dropWidth = menu.innerWidth(), dropHeight = menu.innerHeight();
                    let buttonWidth = dropdownPositioner.outerWidth(), buttonHeight = dropdownPositioner.outerHeight();
                    let position = dropdownPositioner.offset();
                    if (dropButton.data("dropdown-is-fixed")) {
                        position.top -= $(window).scrollTop();
                        position.left -= $(window).scrollLeft();
                    }
                    let xButtonCenter = position.left + buttonWidth / 2;
                    let hor = elDefaults.hor, ver = elDefaults.ver;
                    let x, y;

                    switch (hor) {
                        case "center":
                            if (xButtonCenter + dropWidth / 2 + settings.windowPadding > screenWidth) {
                                if (settings.realign) {
                                    hor = "right";
                                    x = xButtonCenter - dropWidth;
                                } else
                                    x = screenWidth - settings.windowPadding - dropWidth;
                            } else if (xButtonCenter - dropWidth / 2 < settings.windowPadding) {
                                if (settings.realign) {
                                    hor = "left";
                                    x = xButtonCenter;
                                } else
                                    x = settings.windowPadding;
                            } else
                                x = xButtonCenter - dropWidth / 2;
                            break;
                        case "right":
                            if (xButtonCenter - dropWidth < settings.windowPadding) {
                                if (settings.realign) {
                                    if (xButtonCenter - dropWidth / 2 < settings.windowPadding) {
                                        hor = "left";
                                        x = xButtonCenter;
                                    } else {
                                        hor = "center";
                                        x = xButtonCenter - dropWidth / 2;
                                    }
                                } else
                                    x = settings.windowPadding;
                            } else
                                x = xButtonCenter - dropWidth;
                            break;
                        case "left":
                            if (xButtonCenter + dropWidth + settings.windowPadding > screenWidth) {
                                if (settings.realign) {
                                    if (xButtonCenter + dropWidth / 2 + settings.windowPadding > screenWidth) {
                                        hor = "right";
                                        x = xButtonCenter - dropWidth;
                                    } else {
                                        hor = "center";
                                        x = xButtonCenter - dropWidth / 2;
                                    }
                                } else
                                    x = screenWidth - settings.windowPadding - dropWidth;
                            } else
                                x = xButtonCenter;
                            break;
                        default:
                            throw "Unknown horizontal alignment-type: " + hor;
                    }
                    switch (ver) {
                        case "top":
                            if (position.top - settings.elementOffset - dropHeight < settings.windowPadding) {
                                if (settings.realign) {
                                    ver = "bottom";
                                    y = position.top + buttonHeight + settings.elementOffset;
                                } else
                                    y = settings.windowPadding;
                            } else
                                y = position.top - settings.elementOffset - dropHeight;
                            break;
                        case "bottom":
                            if (position.top + buttonHeight + settings.elementOffset +
                                dropHeight + settings.windowPadding > screenHeight) {

                                if (settings.realign) {
                                    ver = "top";
                                    y = position.top - settings.elementOffset - dropHeight;
                                } else
                                    y = screenHeight - settings.windowPadding - dropHeight;
                            } else
                                y = position.top + buttonHeight + settings.elementOffset;
                            break;
                        default:
                            throw "Unknown vertical alignment-type: " + ver;
                    }

                    menuContainer.css({
                        "top": (y - parseFloat(menu.css("border-top-width"))) + "px",
                        "left": (x - parseFloat(menu.css("border-left-width"))) + "px"
                    });
                    menu.removeClass(Object.values(dropdownStyles.ver).join(" ") + " " +
                        Object.values(dropdownStyles.hor).join(" "));

                    menu.addClass(dropdownStyles.ver[ver] + " " + dropdownStyles.hor[hor]);
                });
                break;
            case "hidden":
                return this.data("dropdown-container").css("display") === "none";
            default:
                throw "Unknown action type: " + action;
        }
        return this;
    };
}(jQuery));
