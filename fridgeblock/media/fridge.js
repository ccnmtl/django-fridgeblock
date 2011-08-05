var saveMagnetPosition = function(id,x,y) {
  if (saveURL == "dummy") {
    return;
  }
   var req = new XMLHttpRequest();
   var url = saveURL + "?item_id=" + id + ";x=" + parseInt(x) + ";y=" + parseInt(y);
   req.open("POST",url,true);
   req.send(null);
};

var disableLabel = function(magnet) {
  jQuery("#item-" + magnet.attr("id").split("-")[1] + "-label").addClass("disabled");
  var grabber = jQuery("#item-" + magnet.attr("id").split("-")[1] + "-grabber");
  grabber.addClass("category-icon");
  grabber.removeClass("grabber");
  grabber.draggable("option", "disabled", true);
};

var deleteMagnet = function(elem) {
  var id = elem.parent().attr("id").split("-")[1];
  var magnet = jQuery("[id^=item-" + id + "].magnet");

  // delete from session
  if (deleteURL == "dummy") {
  } else {
    var req = new XMLHttpRequest();
    var url = deleteURL + "?item_id=" + id;
    req.open("POST",url,true);
    req.send(null);
  }


  // hide on fridge -- NOT using display:none so the others stay put
  magnet.css("visibility", "hidden");

  // enable in menu
  jQuery("#item-" + magnet.attr("id").split("-")[1] + "-label").removeClass("disabled");
  var grabber = jQuery("#item-" + magnet.attr("id").split("-")[1] + "-grabber");
  grabber.removeClass("category-icon");
  grabber.addClass("grabber");
  grabber.draggable("option", "disabled", false);

  // hide popup
  elem.parent().hide();
};



jQuery(document).ready(function(){
	jQuery('.category').click(function() {
		jQuery(this).nextUntil("tr.category").toggle();
                jQuery(this).find(".arrow").toggleClass("open");
                jQuery(this).find(".arrow").toggleClass("closed");
		return false;
	}).nextUntil("tr.category").hide();
});

jQuery( function() {
   jQuery(".grabber").draggable({
        revert: 'invalid'
        , appendTo: '#fridge'
        , scroll: false
   });
   jQuery(".grabber-disabled").draggable("option", "disabled", true);

   // we need to use helper:clone for the divs in the menu, because otherwise
   // they can't be dragged out of the overflow:hidden (and also get
   // hidden when the turnbuckle is closed, even if they're on the fridge)
   jQuery(".grabber-in-menu").each(function() {
				     jQuery(this).draggable({
         helper: 'clone'
							    });

     // can't use .width() and .height() before images are loaded
     var width = parseInt(jQuery(this).css('width'));
     var height = parseInt(jQuery(this).css('height'));
     jQuery(this).draggable("option", "cursorAt", {'top': height/2, 'left': width/2});
   });

   jQuery("#fridge").droppable({
     drop: function(event, ui) {
       jQuery(this).addClass('dropped');

       var item = ui.draggable;

       // if we've got a clone, we need to actually save it and put it where it belongs
       if( item.hasClass('grabber-in-menu') ) {
         // if the magnet is already on the fridge (but hidden), just re-use that one
         var magnet = jQuery("#item-" + item.attr('id').split("-")[1] + "-magnet");
         if(magnet.length > 0) {
           magnet.css('visibility', 'visible');
         }
         else {
           magnet = item.clone();
           magnet.attr("id", "item-" + magnet.attr('id').split("-")[1] + "-magnet");
           magnet.removeClass('grabber-in-menu');
           magnet.addClass('magnet');
           magnet.appendTo("#fridge");
         }

         var width = magnet.width();
         var height = magnet.height();
         magnet.offset({'top':event.pageY-height/2 , 'left':event.pageX-width/2 })

         magnet.draggable({
           revert: 'invalid'
           , appendTo: '#fridge'
           , scroll: 'false'
         });
         magnet.click(togglePopup);

         // take its popup label too
         var popup = jQuery("#item-" + magnet.attr('id').split("-")[1] + "-popup");
         popup.appendTo("#fridge");

         item = magnet;  // so the code below saves its position correctly
       }

       // save the magnet's position
       var fridgeOffset = jQuery(this).offset();
       var offset = item.offset();
       var store_x = offset.left - fridgeOffset.left;
       var store_y = offset.top - fridgeOffset.top;
       saveMagnetPosition(item.attr("id").split("-")[1],store_x,store_y);

       disableLabel(item);
       event.stopPropagation();
     }
   });

   jQuery(".magnet-trash").click(function() { deleteMagnet( jQuery(this) ); });
});
