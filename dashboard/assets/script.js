$(".nav a").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).parent().addClass("active");
});

//$.fn.followTo = function (pos) {
//    var $this = this,
//        $window = $(window);
//
//    $window.scroll(function (e) {
//        if ($window.scrollTop() > pos) {
//            $this.css({
//                position: 'absolute',
//                top: pos
//            });
//        } else {
//            $this.css({
//                position: 'fixed',
//                top: 0
//            });
//        }
//    });
//};
//
//$('#test').followTo(250);

//document.getElementById('stats').onclick = function() {
//  var newDiv = document.createElement('div');
//  newDiv.className = '_dash-loading-callback';
//  newDiv.id = 'loading';
//  document.body.appendChild(
//    newDiv,
//    document.getElementById('content'));
//}
