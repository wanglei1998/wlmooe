/**
 * Created by Administrator on 2016/12/17.
 */

$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);
        if(that.children('a').attr('href') == '#'){
            event.preventDefault();
        }
        if(that.parent().hasClass('unfold')){
            that.parent().removeClass('unfold');
        }else{
            that.parent().addClass('unfold').siblings().removeClass('unfold');
        }
        console.log('coming....');
    });

    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration','none');
    });
});


$(function () {
    var url = window.location.href;
    if(url.indexOf('profile') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(0).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('resetpwd') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(1).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('resetemail') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(2).addClass('active').siblings().removeClass('active');
    } else if(url.indexOf('banners') >= 0){
        var bannerManageLi = $('.banner-manage');
        bannerManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('boards') >= 0){
        var boardManageLi = $('.board-manage');
        boardManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('courses') >= 0){
        var courseManageLi = $('.course-manage');
        courseManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('comments') >= 0){
        var commentManageLi = $('.comment-manage');
        commentManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('teacher') >= 0){
        var teacherManageLi = $('.teacher-manage');
        teacherManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('student') >= 0){
        var studentManageLi = $('.student-manage');
        studentManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
});