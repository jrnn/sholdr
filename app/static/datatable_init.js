var hack = $( 'script[src *= datatable_init]' );
var root = hack.attr( 'data-root' );
var tableIds = hack.attr( 'data-tableIds' ).split( ';' );

$( document ).ready( function() {
  $.map( tableIds, function( tableId, i ) {
    $( '#' + tableId ).DataTable( {
      'lengthChange' : false
    } );
    $( '#' + tableId ).on( 'click', 'tbody tr', function() {
      var href = $( this ).data( 'href' );
      if ( href ) {
        window.location.href = root + href;
      }
    });
  });
});
