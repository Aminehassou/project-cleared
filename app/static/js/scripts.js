$( document ).ready(function() {

    $('#autocomplete').autocomplete({
        serviceUrl: "/games",
        onSelect: function (suggestion) {
            console.log(suggestion);
            window.location.replace(suggestion.url);
        }
    });
    $('#edit-game').on('show.bs.modal', function (e) {
        let relatedTarget = $(e.relatedTarget);
        let currentTarget = $(e.currentTarget);

        let gameName = relatedTarget.data('game-name');
        let statusId = relatedTarget.data('status-id');
        let platform = relatedTarget.data('platform');
        let userGameId = relatedTarget.data('user-game-id');
        currentTarget.find('#game-name input').val(gameName);
        currentTarget.find('#status').val(statusId);
        currentTarget.find('#platform input').val(platform);
        currentTarget.find('#user_game_id').val(userGameId);
      })
});

