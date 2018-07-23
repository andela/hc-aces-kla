$(function() {

    $(".member-remove").click(function() {
        var $this = $(this);
        
        $("#rtm-email").text($this.data("email"));
        $("#remove-team-member-email").val($this.data("email"));
        $('#remove-team-member-modal').modal("show");

        return false;
    });

    $(".assign-checks").click(function () {
        var $this = $(this);
        var checks_count = $this.data("checks")
        var forloop_count = $this.data("count")

        var start = forloop_count * checks_count
        var end = ((forloop_count + 1) * checks_count)
        var assign_list = $this.data("checksx")
        console.log(assign_list)
        var compare = []
        for (var i = start; i < end; i++){
            compare.push(assign_list[i])
        }
        console.log(compare)
        function applyFilters(index, element) {
            if (compare[index] == 1){
                $(element).find("input.assigned_test").prop("checked", true);
            }else{
                $(element).find("input.assigned_test").prop("checked", false);
            }
        }

        // Desktop: for each row, see if it needs to be shown or hidden
        $(".assign td.loads2").each(applyFilters);
        
        $("#rtm-email").text($this.data("email"));
        $(".remove-team-member-email").val($this.data("email"));
        $('#assign-check-modal').modal("show");

        

        return false;
    });

});