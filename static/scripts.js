if ($('.grid_cell_profile_actions_profile_picture')) {
    setInterval(()=>{
        let profile_picture = $('.grid_cell_profile_actions_profile_picture')
        profile_picture.height(profile_picture.width())
    }, 10)
}