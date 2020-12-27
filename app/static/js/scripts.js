(function() {

    //var data = ["a", "b", "c"];

    var bh = new Bloodhound({
        remote: {
            url: '/games?query=%QUERY',
            wildcard: '%QUERY'
        },
        limit: 10,
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
    });
    

    $('#autocomplete').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'games',
        source: bh,
        templates: {
            empty: [
                '<div class="ml-1">No results to show</div>'
            ],
            pending: '<div class="ml-1">Loading results...</div>',
            suggestion: function(data) {
                console.log(data);
                return `<div><img src="https://images.igdb.com/igdb/image/upload/t_cover_small/${data.image_id}.jpg" height="50"> ${data.name}</div>`;
            }
        }
    });

    let selectedName = '';
    let gameUrl = '';
    $('#autocomplete').bind('typeahead:select', function (ev, suggestion) {
        console.log("suggestion", suggestion);
        selectedName = suggestion.name;
        gameUrl = suggestion.url;
    });
    $('#autocomplete').bind('typeahead:close', function (obj) {
        let currTarget = $(obj.currentTarget);
        console.log("closed");
        currTarget.val(selectedName);
        window.location.replace(gameUrl);
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
})();

