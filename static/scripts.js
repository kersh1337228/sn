if ($('.grid_cell_profile_actions_profile_picture')) {
    setInterval(()=>{
        let profile_picture = $('.grid_cell_profile_actions_profile_picture')
        profile_picture.height(profile_picture.width())
    }, 10)
}

if($('.attach')) {
    // attach button interaction animation
    $('.content').on('click', '.attach', function() {
        let attach_menu = $(this).parent().children('.attach_menu')
        if (attach_menu.css('visibility') === 'visible') {
            attach_menu.css('visibility', 'hidden')
            attach_menu.css('opacity', '0')
            attach_menu.css('transform', 'translate(-20%, 0%)')
        } else {
            attach_menu.css('visibility', 'visible')
            attach_menu.css('opacity', '1')
            attach_menu.css('transform', 'translate(-20%, 70%)')
        }
    })
    // attach_menu.mouseover(attach_menu_switch)

    // attach menu buttons functional
    $('.attach_menu_image').click(()=>{$('#id_images').click()})
    $('.attach_menu_video').click(()=>{$('#id_videos').click()})
    $('.attach_menu_audio').click(()=>{$('#id_audios').click()})
    $('.attach_menu_file').click(()=>{$('#id_files').click()})
    $('.content').on('click', '.send_message_icon', function() {
        $(this).parent().children('button').click()
    })
}

// textarea automatic height correction
if ($('textarea')) {
    // let textarea = $('textarea')
    // let textarea_size = function() {
    //     if ($(this).outerHeight() > this.scrollHeight) {
    //         $(this).height(1)
    //     }
    //     while ($(this).outerHeight() < this.scrollHeight) {
    //         $(this).height($(this).height() + 1)
    //     }
    // }
    // textarea.on('paste input', textarea_size)
    //
    $("textarea").each(function () {
        // this.setAttribute("style", "height:" + (this.scrollHeight) + "px;");
        this.style.height = (this.scrollHeight * 0.8) + "px";
    }).on("paste input", function () {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight * 0.8) + "px";
    });
    $('textarea').trigger('input')
}

if($('.message_edit')) {
    // message edit button interaction animation
    let message_edit_button = $('.message_edit')
    let message_edit_menu = $('.message_edit_menu')
    let message_edit_menu_switch = function (){
        let message_edit_menu = $(this)[0].lastElementChild
        if (message_edit_menu.style.visibility === 'visible') {
            message_edit_menu.style.visibility = 'hidden'
            message_edit_menu.style.opacity = '0'
            message_edit_menu.style.transform = 'translate(-15px, -100%)'
        } else {
            message_edit_menu.style.visibility = 'visible'
            message_edit_menu.style.opacity  = '1'
            message_edit_menu.style.transform = 'translate(-15px, -140%)'
        }
    }
    $('.chat_content_grid_cell_messages').on('click', '.message_edit', message_edit_menu_switch)
    // message_edit_button.on('click', message_edit_menu_switch)
    // attach_menu.mouseover(attach_menu_switch)
}

if ($('.note_edit')) {
    // note edit button interaction animation
    let note_edit_button = $('.note_edit')
    let note_edit_menu = $('.note_edit_menu')
    let note_edit_menu_switch = function (){
        let note_edit_menu = $(this)[0].lastElementChild
        if (note_edit_menu.style.visibility === 'visible') {
            note_edit_menu.style.visibility = 'hidden'
            note_edit_menu.style.opacity = '0'
            note_edit_menu.style.transform = 'translate(0, -100%)'
        } else {
            note_edit_menu.style.visibility = 'visible'
            note_edit_menu.style.opacity  = '1'
            note_edit_menu.style.transform = 'translate(0, -170%)'
        }
    }
    note_edit_button.click(note_edit_menu_switch)
    // attach_menu.mouseover(attach_menu_switch)
}


if ($('.comment_icon')) {
    let comment_button = $('.comment_icon')
    let comment_menu_switch = function (){
        let comment_menu = $(this)[0].parentElement.parentElement.parentElement.lastElementChild
        if (comment_menu.style.visibility === 'visible') {
            comment_menu.style.display = 'none'
            comment_menu.style.maxHeight = '0'
            comment_menu.style.visibility = 'hidden'
            comment_menu.style.opacity = '0'
            // comment_menu.style.transform = 'translate(0, -105%)'
        } else {
            comment_menu.style.display = 'grid'
            comment_menu.style.maxHeight = '100%'
            comment_menu.style.visibility = 'visible'
            comment_menu.style.opacity  = '1'
            // comment_menu.style.transform = 'translate(0, 0%)'
        }
    }
    comment_button.click(comment_menu_switch)
}


if ($('.reply_icon')) {
    let reply_button = $('.reply_icon')
    let reply_menu_switch = function (){
        let reply_menu = $(this)[0].parentElement.parentElement.parentElement.lastElementChild
        if (reply_menu.style.visibility === 'visible') {
            reply_menu.style.display = 'none'
            reply_menu.style.maxHeight = '0'
            reply_menu.style.visibility = 'hidden'
            reply_menu.style.opacity = '0'
            // comment_menu.style.transform = 'translate(0, -105%)'
        } else {
            reply_menu.style.display = 'grid'
            reply_menu.style.maxHeight = '100%'
            reply_menu.style.visibility = 'visible'
            reply_menu.style.opacity  = '1'
            // comment_menu.style.transform = 'translate(0, 0%)'
        }
    }
    reply_button.click(reply_menu_switch)
}

if ($('#search_button')) {
    $('.search_icon').click(()=> {
        $('#search_button').click()
    })
}
