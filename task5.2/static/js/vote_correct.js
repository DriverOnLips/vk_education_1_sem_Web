function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function sendCorrectVoteRequest(answer_id, is_correct, csrf_token) {
  const formData = new FormData();
  formData.append('answer_id', answer_id);
  formData.append('is_correct', is_correct);
  formData.append('csrfmiddlewaretoken', csrf_token);
  const request = new Request('/vote_correct/', {method: 'POST', body: formData});
  return fetch(request).then(
      response_raw => response_raw.json().then(
          response_json => $('#correct-' + response_json.answer_id).prop('checked', response_json.is_correct)
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