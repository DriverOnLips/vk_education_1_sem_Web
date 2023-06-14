function sendAnswerVoteRequest(answer_id, mark_name, csrf_token) {
  const formData = new FormData();
  formData.append('answer_id', answer_id);
  formData.append('mark_name', mark_name);
  formData.append('csrfmiddlewaretoken', csrf_token);
  const request = new Request('/vote_answer/', {method: 'POST', body: formData});
  return fetch(request).then(
      response_raw => response_raw.json().then(
          response_json => $('.likes#' + answer_id).text(response_json.new_rating)
      )
  );
}

$(".answer-dislike-btn").on('click', function (ev) {
    const answer_id = $(this).attr('id').split('-')[2];
    const csrf_token = csrftoken;
    if ($(this).hasClass("answer-dislike-btn")) {
        sendAnswerVoteRequest(answer_id, 'dislike', csrf_token);
    } else {
        sendAnswerVoteRequest(answer_id, '', csrf_token);
    }
});

$(".answer-like-btn").on('click', function (ev) {
    const answer_id = $(this).attr('id').split('-')[2];
    const csrf_token = csrftoken;
    if ($(this).hasClass("answer-like-btn")) {
        sendAnswerVoteRequest(answer_id, 'like', csrf_token);
    } else {
        sendAnswerVoteRequest(answer_id, '', csrf_token);
    }
});

