// Chat send message ajax
$('form').submit(function (page) {
        page.preventDefault()
        console.log('WORKS')
        let serializedData = $(this).serialize()
        let url_list = location.href.split('/')
        let chat_id = url_list[url_list.length - 2]
        $.ajax({
            type: 'POST',
            url: `{% url 'private_chat' chat_id=${chat_id} %}`,
            data: serializedData,
            success: function (response) {
                $('form').trigger('reset')
            },
            error: function (response) {
                alert(response["responseJSON"]["error"])
            }
        })
})