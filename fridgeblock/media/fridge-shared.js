var positionMagnet = function(magnet,x,y) {
   var fridgeOffset = jQuery("#fridge").offset();
   fridgeOffset.left = fridgeOffset.left + x;
   fridgeOffset.top  = fridgeOffset.top + y;
   magnet.offset(fridgeOffset);
};

function togglePopup() {
  // destroy any existing popups
  jQuery(".magnet-popup").hide();

  // position popup correctly
  var id = jQuery(this).attr("id");
  var popup = jQuery("#" + id.substr(0, id.length-7) + "-popup");
  var windowOffsetTop = jQuery(window).scrollTop();
  var windowOffsetLeft = jQuery(window).scrollLeft();
  var fridgeOffset = jQuery("#fridge").offset()
  /* popup.offset(...) is buggy in Chrome */
  //popup.offset({'top': jQuery(this).offset().top - fridgeOffset.top - popup.height() + windowOffsetTop + 20,
  //              'left': jQuery(this).offset().left - fridgeOffset.left - popup.width() + windowOffsetLeft - 20 });
  popup.css('top', jQuery(this).offset().top - fridgeOffset.top - popup.height() + windowOffsetTop + 20);
  popup.css('left', jQuery(this).offset().left - fridgeOffset.left - popup.width() + windowOffsetLeft - 20);
  jQuery(popup).show();
}

jQuery(document).ready(function(){
  jQuery(".magnet").click(togglePopup);
  jQuery(".magnet-popup-close").click(function() { jQuery(this).parent(".magnet-popup").hide(); });
});