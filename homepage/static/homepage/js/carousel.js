
$(function () {
    const velocity = 120; // in px/s

    $(".carousel").each(function () {
        let innerHTML = $(this).html();
        $(this).html("<div class='carousel-container'>" + innerHTML + "</div>");
        let container = $("> .carousel-container", this).addClass("animate");
        let items = $("> .carousel-items", container);
        container.append(items.clone());
        let itemsWidth = items.outerWidth();
        container.css("width", 2 * itemsWidth + "px");
        container.timedHover(function () {
            container.css("animation-play-state", "paused");
        }, function () {
            container.css("animation-play-state", "");
        });

        container.css("animation", "carousel-anim " + (itemsWidth / velocity) + "s linear infinite");
    });
    $(window).on("resize", function () {
        $(".carousel > .carousel-container").each(function () {
            $(this).css("width", 2 * $("> .carousel-items", this).outerWidth() + "px");
        });
    });
});
