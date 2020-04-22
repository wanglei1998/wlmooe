/**
 * Created by hynev on 2018/1/3.
 */

$(function () {
    var ue = UE.getEditor("editor",{
        'serverUrl': '/ueditor/upload/',
        "toolbars": [
            [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'source', //源代码
                'blockquote', //引用
                'selectall', //全选
                'insertcode', //代码语言
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传
                'emotion' //表情
            ]
        ]
    });
    window.ue = ue;
});

$(function () {
    $("#comment-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            window.location = '/signin/';
        }else{
            var content = window.ue.getContent();
            var course_id = $("#course-content").attr("data-id");
            zlajax.post({
                'url': '/acomment/',
                'data':{
                    'content': content,
                    'course_id': course_id
                },
                'success': function (data) {
                    if(data['code'] == 200){
                        window.location.reload();
                    }else{
                        zlalert.alertInfo(data['message']);
                    }
                }
            });
        }
    });
});


$(function () {
    //评分
    var starRating = 0;
    var index = 0;
    var s = "未进行评分";
    $('.photo span').on('mouseenter', function () {
        index = $(this).index() + 1;
        $(this).prevAll().find('.high').css('z-index', 1)
        $(this).find('.high').css('z-index', 1)
        $(this).nextAll().find('.high').css('z-index', 0)
        if (index == 1) {
            s = "非常不满意";
        } else if (index == 2) {
            s = "不满意"
        } else if (index == 3) {
            s = "一般"
        } else if (index == 4) {
            s = "满意"
        } else {
            s = "非常满意"
        }
        //$('.starNum').html((index*2).toFixed(1)+'分')
        $('.starNum').html(s)
    })
    $('.photo').on('mouseleave', function () {
        $(this).find('.high').css('z-index', 0)
        var count = starRating / 2
        if (count == 5) {
            $('.photo span').find('.high').css('z-index', 1);
        } else {
            $('.photo span').eq(count).prevAll().find('.high').css('z-index', 1);
        }
        //$('.starNum').html(starRating.toFixed(1)+'分')
        $('.starNum').html(s)
    })
    $('.photo span').on('click', function () {
        var index = $(this).index() + 1;
        $(this).prevAll().find('.high').css('z-index', 1)
        $(this).find('.high').css('z-index', 1)
        $('.starNum').html(s);
        starRating = index * 2;
        //$('.starNum').html(starRating.toFixed(1)+'分');
        //alert('评分：'+(starRating.toFixed(1)+'分'))
    })
//取消评分
    $('.cancleStar').on('click', function () {
        starRating = 0;
        $('.photo span').find('.high').css('z-index', 0);
        //$('.starNum').html(starRating.toFixed(1)+'分');
        $('.starNum').html('未进行评分')
    })
//确定评分
    $('.sureStar').on('click', function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        var course_id = $("#course-content").attr("data-id");
        if(!loginTag){
            window.location = '/signin/';
        }else{
            if (starRating === 0) {
            alert('请点击上方星星');
            } else {
                alert('评分：' + s)
                //alert('评分：'+(starRating.toFixed(1)+'分'))
                zlajax.post({
                'url': '/astar/',
                'data':{
                    'course_id':course_id,
                    'index': index
                },
                'success': function (data) {
                    if(data['code'] == 200){
                        window.location.reload();
                    }else{
                        zlalert.alertInfo(data['message']);
                    }
                }
            });
            }
        }

    })
})
