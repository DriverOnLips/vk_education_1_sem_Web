function sendCorrectVoteRequest(answer_id, is_correct, csrf_token) {
  const $checkbox = $('#correct-' + answer_id);
  const formData = new FormData();
  formData.append('answer_id', answer_id);
  formData.append('is_correct', Boolean(is_correct));
  formData.append('csrfmiddlewaretoken', csrf_token);
  const request = new Request('/vote_correct/', {method: 'POST', body: formData});
  return fetch(request).then(
      response_raw => response_raw.json().then(
          response_json => {
            $checkbox.prop('checked', response_json.is_correct);
          }
      )
  );
}

$(".form-check-input").on('click', function (ev) {
    const answer_id = $(this).attr('id');
    const csrf_token = csrftoken;
    let is_correct = false;
    if ($(this).is(':checked')) {
        is_correct = true;
    }
    if ($(this).hasClass("form-check-input")) {
        sendCorrectVoteRequest(answer_id, is_correct, csrf_token);
    } else {
        sendCorrectVoteRequest(answer_id, is_correct, csrf_token);
    }
});