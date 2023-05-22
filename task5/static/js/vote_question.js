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

function sendQuestionVoteRequest(question_id, mark_name, csrf_token) {
  const formData = new FormData();
  formData.append('question_id', question_id);
  formData.append('mark_name', mark_name);
  formData.append('csrfmiddlewaretoken', csrf_token);
  const request = new Request('/vote_question/', {method: 'POST', body: formData});
  return fetch(request).then(
      response_raw => response_raw.json().then(
          response_json => $('.likes#' + question_id).text(response_json.new_rating)
      )
  );
}

$(".question-like-btn").on('click', function (ev) {
    const question_id = $(this).attr('id').split('-')[2];
    const csrf_token = csrftoken;
    if ($(this).hasClass("question-like-btn")) {
        sendQuestionVoteRequest(question_id, 'like', csrf_token);
    } else {
        sendQuestionVoteRequest(question_id, '', csrf_token);
    }
});

$(".question-dislike-btn").on('click', function (ev) {
    const question_id = $(this).attr('id').split('-')[2];
    const csrf_token = csrftoken;
    if ($(this).hasClass("question-dislike-btn")) {
        sendQuestionVoteRequest(question_id, 'dislike', csrf_token);
    } else {
        sendQuestionVoteRequest(question_id, '', csrf_token);
    }
});

