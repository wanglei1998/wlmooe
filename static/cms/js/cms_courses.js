/**
 * Created by King on 2020/4/21.
 */



$(function () {

    $(".highlight-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var course_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if(highlight){
            url = "/cms/uhpost/";
        }else{
            url = "/cms/hpost/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'course_id': course_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });

    $(".delete-course-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var course_id = tr.attr('data-id');
        zlalert.alertConfirm({
            "msg":"您确定要删除这门课程吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dcourse/',
                    'data':{
                        'course_id': course_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            zlalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});
