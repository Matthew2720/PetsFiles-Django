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
        var id = data.results[i].idProduct;
        var name = data.results[i].full_name;
        var stock = data.results[i].stock;
        var pvp = data.results[i].pvp;
        if (stock > 1) {
          results += '<tr data-id="' + id + '" data-name="' + name + '" data-stock="' + stock + '" data-pvp="' + pvp + '"><td>' + name + '</td><td>' + stock + '</td><td>' + pvp + '</td></tr>';
        }
      }
      response(data.results);
    }
  });
},
    minLength: 1,
    select: function(event, ui) {
      var selectedProduct = ui.item;
      var id = selectedProduct.idProduct;
      var name = selectedProduct.full_name;
      var stock = selectedProduct.stock;
      var pvp = selectedProduct.pvp;
      var inputQuantity = $('<input>').attr({
        type: 'number',
        min: '0',
        max: stock, // La cantidad máxima es igual al stock
        value: '0',
      });
      var newRow = $('<tr>').attr({
        'data-id': id,
        'data-name': name,
        'data-stock': stock,
        'data-pvp': pvp
      }).append($('<td>').text(name))
        .append($('<td>').text(stock))
        .append($('<td>').text(pvp))
        .append($('<td>').append(inputQuantity))
        .append($('<td>').append($('<input>').attr({
        type: 'number',
        min: '0',
        max: '100',
        value: '19', // Valor por defecto del IVA
        class: 'iva-input'})))
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

  $('#cart tbody').on('change', 'input[type="number"]', function() {
    var stock = $(this).closest('tr').data('stock');
    if ($(this).val() > stock) {
      $(this).val(stock);
    }
    var quantity = $(this).val();
    var pvp = $(this).closest('tr').data('pvp');
    var iva = $(this).closest('tr').find('.iva-input').val();
    var subtotal = quantity * (pvp + (pvp * (iva/100)));
    $(this).closest('tr').find('.subtotal').text(subtotal.toFixed(0));
    updateSubtotal();
  });

  $('#cart tbody').on('click', 'button', function() {
    $(this).closest('tr').remove();
    updateSubtotal();
  });

  function updateSubtotal() {
    var subtotal = 0;
    var totalIva = 0;
    $('#cart tbody tr').each(function() {
      var quantity = $(this).find('input[type="number"]').val();
      var pvp = $(this).data('pvp');
      var iva = $(this).find('.iva-input').val();
      var rowTotalIva = pvp * iva / 100 * quantity;
      totalIva += rowTotalIva;
      var rowSubtotal = pvp * quantity + rowTotalIva;
      subtotal += rowSubtotal;
      $(this).find('.subtotal').text(rowSubtotal.toFixed(0));
    });
    $('#totalIva').text(totalIva.toFixed(0));
    $('#total').text(subtotal.toFixed(0));
  }

  function createCartJson() {
      var products = [];
      var totalIva = 0;

      $('#cart tbody tr').each(function() {
          var id = $(this).data('id');
          var name = $(this).data('name');
          var quantity = $(this).find('input').val();
          var pvp = $(this).data('pvp');
          var iva = $(this).find('.iva-input').val();
          var productIva = pvp * iva / 100;
          var rowSubtotal = 0;

          totalIva += productIva * quantity;

          var product = {
              'id': id,
              'name': name,
              'quantity': quantity,
              'pvp': pvp,
              'iva': iva,
              'subtotal': rowSubtotal.toFixed(0)
          };
          products.push(product);
      });

      var cartJson = {
          'products': products,
          'total': parseFloat($('#total').text()),
          'total_iva': totalIva.toFixed(0)
      };

      return cartJson;
  }

  $('#send-json').click(function() {
    var cartJson = createCartJson();
    console.log(cartJson); // muestra el json en la consola
    var csrfToken = $('#sale-form [name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: "/procesar/factura",
        type: "POST",
        dataType: "json",
        data: JSON.stringify(cartJson),
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(data) {
            alert('Datos enviados');
            window.location.replace('/registrar/venta');
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    })
});

});

