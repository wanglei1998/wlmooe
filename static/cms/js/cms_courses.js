/**
 * Created by King on 2020/4/21.
 */
$(function () {
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
