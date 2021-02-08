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
    

    $('.autocomplete').typeahead({
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
                return `<div><img src="${data.image_url}" height="50"> ${data.name}</div>`;
            }
        }
    });

    let selectedName = '';
    let gameUrl = '';
    $('.autocomplete').bind('typeahead:select', function (ev, suggestion) {
        console.log("suggestion", suggestion);
        selectedName = suggestion.name;
        gameUrl = suggestion.url;
    });
    $('.autocomplete').bind('typeahead:close', function (obj) {
        let currTarget = $(obj.currentTarget);
        console.log("closed");
        currTarget.val(selectedName);
        window.location.replace(gameUrl);
    });
    $('.autocomplete').bind('typeahead:cursorchange', function (obj, suggestion) {
        let currTarget = $(obj.currentTarget);
        console.log("cursorchange");
        currTarget.val(suggestion.name);

    });


    $('#edit-game').on('show.bs.modal', function (e) {
        let relatedTarget = $(e.relatedTarget);
        let currentTarget = $(e.currentTarget);

        let gameName = relatedTarget.data('game-name');
        let statusId = relatedTarget.data('status-id');
        let platform = relatedTarget.data('platform');
        let userGameId = relatedTarget.data('user-game-id');
        let userGameNote = relatedTarget.data('user-game-note');
        currentTarget.find('#game-name input').val(gameName);
        currentTarget.find('#status').val(statusId);
        currentTarget.find('#platform input').val(platform);
        currentTarget.find('#note').val(userGameNote);
        currentTarget.find('#user_game_id').val(userGameId);
      })
    $('.delete-game').on('click', function (e) {
        if (confirm('Are you sure you want to delete this game from your list?')) {
            // Delete it!
            let target = $(e.currentTarget);
            target.next('form').submit();
            console.log('Game Deleted');
          } else {
            // Do nothing!
            console.log('Game Not Deleted');
          }
    })

})();

