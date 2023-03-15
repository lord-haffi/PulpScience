"use strict";

$(function () {
    $(".nav:has(.nav-menu-collapsible)").each(function () {
        //let height = $(this).outerHeight();
        let collapsibleMenus = $(".nav-menu-collapsible", this);
        collapsibleMenus.each(function () {
            //$(this).css("top", height + "px");
            let menu = $("> div", this);
            //menu.addClass("hide");
            $("> .expander", this).click(function () {
                if (menu.css("display") === "block") {
                    // Slide down
                    menu.addClass("expanded");
                    menu.removeClass("hide");
                    // setTimeout(function () {
                    //     menu.removeClass("slide-point-0");
                    // }, 10); // A little hack to trigger transition animation
                } else {
                    // Slide up
                    menu.addClass("hide");
                    // menu.addClass("slide-point-0");
                    setTimeout(function () {
                        menu.removeClass("expanded");
                    }, 400);
                }
            });
        });
        $(this).data("nav-collapsible-menus", collapsibleMenus);
    });

    let navUser = $(".nav-user"), navTop = $(".nav-top");
    //let navTopCollapsible = navTop.data("nav-collapsible-menus");
    let lastScrollPos = $(window).scrollTop();
    let minimized = false;
    $(window).scroll(function (event) {
        let curScrollPos = $(this).scrollTop();
        if (lastScrollPos < curScrollPos && !minimized) {
            // scrolled down and nav isn't minimized
            navUser.slideUp(200);
            $(".dropdown", navUser).dropdown("hide");
            navTop.addClass("minimized");

            minimized = true;
        } else if (lastScrollPos > curScrollPos && minimized) {
            // scrolled up and nav is minimized
            setTimeout(function () {
                navUser.slideDown(200);
            }, 200);
            navTop.removeClass("minimized");

            minimized = false;
        }
        lastScrollPos = curScrollPos;
    });

    //$(".nav-menu.collapsible").prepend("");
    // let svgHoverFuncs = (function () {
    //     let pathEl = $(".logo svg path");
    //     let stdColor = pathEl.css("fill");
    //     return [
    //             function () {
    //                 $(this).animate({
    //                     fill: "#ef8376",
    //                     stroke: "#ef8376"
    //                 }, 350);
    //             },
    //             function () {
    //                 $(this).animate({
    //                     fill: stdColor,
    //                     stroke: stdColor
    //                 }, 350);
    //             }
    //         ];
    // })();
    // $(".logo svg path").hover(svgHoverFuncs[0], svgHoverFuncs[1]);
    function setActiveCategory(newActiveDOM) {
        $("#sidebar .nav-menu-collapsible a.topic-link.active").removeClass("active");
        if (newActiveDOM) {
            newActiveDOM.addClass("active");
        }
    }
    let currentActiveDOM = $("#sidebar .nav-menu-collapsible a.topic-link.active");
    if (currentActiveDOM) {
        window.history.replaceState({category: currentActiveDOM.text()}, "");
    } else {
        window.history.replaceState({category: undefined}, "");
    }
    window.onpopstate = function (event) {
        let serialized_data = event.state;
        if (serialized_data.category) {
            document.title = "Pulp Science - " + serialized_data.category;
        } else {
            document.title = "Pulp Science";
        }
        setActiveCategory(
            $("#sidebar .nav-menu-collapsible a.topic-link:contains('" + serialized_data.category + "')")
        );
    };
    $("#sidebar .nav-menu-collapsible a.topic-link").each(function () {
        $(this).click(function () {
            let newActive = $(this);
            let newActiveCategory = newActive.text();
            setActiveCategory(newActive);
            window.history.pushState(
                {category: newActiveCategory},
                " - " + newActiveCategory,
                newActive.attr("data-url")
            );
            document.title = "Pulp Science - " + newActiveCategory;
        });
    });
});
