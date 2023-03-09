$(document).ready(function() {
  var products = [];

  $('#search-input').autocomplete({
    source: function(request, response) {
      $.ajax({
        url: '/search/',
        dataType: 'json',
        data: {
          term: request.term
        },
        success: function(data) {
          var results = '';
          for (var i = 0; i < data.results.length; i++) {
            var name = data.results[i].full_name;
            var stock = data.results[i].stock;
            var pvp = data.results[i].pvp;
            results += '<tr data-name="' + name + '" data-stock="' + stock + '" data-pvp="' + pvp + '"><td>' + name + '</td><td>' + stock + '</td><td>' + pvp + '</td></tr>';
          }
          response(data.results);
        }
      });
    },
    minLength: 3,
    select: function(event, ui) {
      var selectedProduct = ui.item;
      var name = selectedProduct.full_name;
      var stock = selectedProduct.stock;
      var pvp = selectedProduct.pvp;
      var inputQuantity = $('<input>').attr({
        type: 'number',
        min: '1',
        max: stock, // La cantidad máxima es igual al stock
        value: '1'
      });
      var newRow = $('<tr>').attr({
        'data-name': name,
        'data-stock': stock,
        'data-pvp': pvp
      }).append($('<td>').text(name))
        .append($('<td>').text(stock))
        .append($('<td>').text(pvp))
        .append($('<td>').append(inputQuantity))
        .append($('<td>').text(pvp).addClass('subtotal'))
        .append($('<td>').append($('<button>').text('Eliminar').addClass("btn btn-danger").click(function(){
            $(this).closest('tr').remove();
            updateSubtotal();
        })));
      $('#cart tbody').append(newRow);
      updateSubtotal();
    }
  }).autocomplete('instance')._renderItem = function(ul, item) {
    return $('<li>')
      .append('<div>' + item.full_name + ' - ' + item.stock + ' unidades</div>')
      .appendTo(ul);
  };

  $('#cart tbody').on('change', 'input', function() {
    var quantity = $(this).val();
    var pvp = $(this).closest('tr').data('pvp');
    var subtotal = quantity * pvp;
    $(this).closest('tr').find('.subtotal').text(subtotal.toFixed(2));
    updateSubtotal();
  });

  $('#cart tbody').on('click', 'button', function() {
    $(this).closest('tr').remove();
    updateSubtotal();
  });

  function updateSubtotal() {
    var subtotal = 0;
    $('#cart tbody tr').each(function() {
      var quantity = $(this).find('input').val();
      var pvp = $(this).data('pvp');
      var rowSubtotal = quantity * pvp;
      subtotal += rowSubtotal;
    });
    $('#subtotal').text(subtotal.toFixed(2));
  }
});

