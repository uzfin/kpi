$(document).ready(function() {
    $('#kpiSelect').change(function() {
        var kpiId = $(this).val();
        $.ajax({
            url: '/dashboard/get-metrics/',
            type: 'GET',
            data: {
                'kpi_id': kpiId
            },
            success: function(data) {
                populateMetrics(data);
            }
        });
    });

    function populateMetrics(metrics) {
        var metricSelect = $('#metricSelect');
        metricSelect.empty(); // Clear previous options
        $.each(metrics, function(index, metric) {
            metricSelect.append($('<option>', {
                value: metric.id,
                text: metric.name
            }));
        });
    }
});