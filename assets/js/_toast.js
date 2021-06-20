$(document).ready(function() {
    $(".toast-header .btn-close").on('click', function(e) {
        console.log(e)
        $target = $(e.target)
        $pparent = $target.parent().parent()
        $pparent.removeClass("show")
        $pparent.addClass("hide")
        console.log($pparent);
    })
})

function _toastCloseButtonHandler() {
}