if ($('.grid_cell_profile_actions_profile_picture')) {
    setInterval(()=>{
        let profile_picture = $('.grid_cell_profile_actions_profile_picture')
        profile_picture.height(profile_picture.width())
    }, 10)
}

if($('.attach')) {
    // attach button interaction animation
    let attach_button = $('.attach')
    let attach_menu = $('.attach_menu')
    let attach_menu_switch = function() {
        let attach_menu = $(this)[0].lastElementChild
        if (attach_menu.style.visibility === 'visible') {
            attach_menu.style.visibility = 'hidden'
            attach_menu.style.opacity = '0'
            attach_menu.style.transform = 'translate(0, -100%)'
        } else {
            attach_menu.style.visibility = 'visible'
            attach_menu.style.opacity  = '1'
            attach_menu.style.transform = 'translate(0, -140%)'
        }
    }
    attach_button.click(attach_menu_switch)
    // attach_menu.mouseover(attach_menu_switch)

    // attach menu buttons functional
    $('.attach_menu_image').click(()=>{$('#id_images').click()})
    $('.attach_menu_video').click(()=>{$('#id_videos').click()})
    $('.attach_menu_audio').click(()=>{$('#id_audios').click()})
    $('.attach_menu_file').click(()=>{$('#id_files').click()})
    $('.send_message_icon').click(function() {
        try {
            $(this)[0].parentElement.children.namedItem('note_btn').click()
        } catch (err) {
            $(this)[0].parentElement.children.namedItem('comment_btn').click()
        }
    })
}

// textarea automatic height correction
if ($('textarea')) {
    $('textarea').on('paste input', function() {
        if ($(this).outerHeight() > this.scrollHeight) {
            $(this).height(1);
        }
        while ($(this).outerHeight() < this.scrollHeight) {
            $(this).height($(this).height() + 1);
        }
    });
}

if($('.message_edit')) {
    // message edit button interaction animation
    let message_edit_button = $('.message_edit')
    let message_edit_menu = $('.message_edit_menu')
    let message_edit_menu_switch = function (){
        let message_edit_menu = $(this)[0].lastElementChild
        console.dir(message_edit_menu)
        if (message_edit_menu.style.visibility === 'visible') {
            message_edit_menu.style.visibility = 'hidden'
            message_edit_menu.style.opacity = '0'
            message_edit_menu.style.transform = 'translate(0, -100%)'
        } else {
            message_edit_menu.style.visibility = 'visible'
            message_edit_menu.style.opacity  = '1'
            message_edit_menu.style.transform = 'translate(0, -170%)'
        }
    }
    message_edit_button.click(message_edit_menu_switch)
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
