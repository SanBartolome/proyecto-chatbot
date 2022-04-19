function submit_message(message) {
    $.post( "/send", {message: message}, handle_response);
  
    function handle_response(data) {
      // append the bot repsonse to the div
      $('.contenedor').append(`
        <div class="chat col-md-5 offset-md-7 bot">
          ${data.message}
        </div>
      `)
    
    // quitar texto de carga
    $( "#loading" ).remove();
  
    if (message == 'Yakarta') {
      $('#input_text').val('Fin del demo')
    }
    else $('#input_text').attr('disabled', false);
  
    }
  }
  
  $('#target').on('submit', function(e){
    e.preventDefault();
    const input_text = $('#input_text').val()
    
    // return if the user does not enter any text
    if (!input_text) {
      return
    }
  
    $('.contenedor').append(`
      <div class="chat col-md-5 respuesta">
        ${input_text}
      </div>
    `)
  
    // cargando 
    $('.contenedor').append(`
      <div class="chat text-center col-md-2 offset-md-10 bot" id="loading">
      <b>...</b>
      </div>
    `)
  
    // limpiar input
    $('#input_text').val('')
  
    $('#input_text').attr('disabled', true);
    
    // enviar mensaje
    submit_message(input_text)
    
  });