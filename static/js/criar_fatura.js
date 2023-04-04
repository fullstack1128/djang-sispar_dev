$(document).ready(function () {
  var $cnpj = $('input[name=cnpj]')
  $cnpj.mask('00.000.000/0000-00', { reverse: true })
})

$(document).ready(function () {
  $('input[type="radio"]').click(function () {
    let inputValue = $(this).attr('value')
    let targetBox = $('#parcelamento_fields')
    let entrada = $('#id_valor_entrada')
    let parcelas = $('#id_numero_parcelas')
    if (inputValue == 'True') {
      $(targetBox).hide()
      $(entrada).removeAttr('required')
      $(parcelas).removeAttr('required')
    } else {
      $(targetBox).show()
      $(entrada).prop('required', true)
      $(parcelas).prop('required', true)
    }
  })
})

function updateValorFinal() {
  let valor_final =
    $('#valor').val() - ($('#id_desconto').val() / 100) * $('#valor').val()
  $('#valor_final').text(
    valor_final.toLocaleString('pt-br', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  )
}

$(document).ready(function () {
  $('input[name=cnpj]').blur(function () {
    var cnpj = $(this).val()

    function limpa_formulário() {
      // Limpa valores do formulário de cep.
      $('#empresa').val('')
      $('#valor').val('')
      $('#inscricao').val('')
    }

    if (cnpj) {
      $('#empresa').val('...')
      $('#valor').val('...')
      $('#inscricao').val('...')

      var url = '/admin/consulta-cnpj/?cnpj=' + cnpj
      $.getJSON(url, function (json) {
        for (item in json) {
          console.log(item.situacaoDescricao)
        }
        const fatura = json[0]
        let total = 0
        json.forEach((item) => {
          total += parseFloat(
            fatura.valorTotalConsolidadoMoeda
              .replaceAll('.', '')
              .replaceAll(',', '.')
          )
        })
        $('#empresa').val(fatura.nomeDevedor)
        $('#valor').val(total.toFixed(2))
        $('#inscricao').val(fatura.numeroInscricao)
      })
    }

    updateValorFinal()
  })
})

updateValorFinal()

$('#id_desconto').on('input', function () {
  updateValorFinal()
})

$('#valor').on('input', function () {
  updateValorFinal()
})
