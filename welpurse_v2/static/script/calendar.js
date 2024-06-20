$(document).ready(function() {
    var calendarEl = document.getElementById('calendar'); // Define the calendar element
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      editable: true, // 'editable' should be inside the options object
      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,agendaWeek,agendaDay'
      },
      events: [{% for row in calendar %}{ id : '{{row.id}}', title : '{{row.title}}', start : '{{row.start_event}}', end : '{{row.end_event}}' }, {% endfor %}],
      selectable: true,
      selectHelper: true,
      select: function(start, end, allDay) {
        var title = prompt("Enter Event Title");
        if (title) {
          var start = FullCalendar.formatDate(start, "Y-MM-DD HH:mm:ss"); // Use FullCalendar.formatDate
          var end = FullCalendar.formatDate(end, "Y-MM-DD HH:mm:ss");
          $.ajax({
            url: "/insert",
            type: "POST",
            data: { title: title, start: start, end: end },
            success: function(data) {
              alert("Added Successfully");
              window.location.replace("/");
            }
          });
        }
      },
      eventResize: function(event) {
        var start = FullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
        var end = FullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");
        var title = event.title;
        var id = event.id;
        $.ajax({
          url: "/update",
          type: "POST",
          data: { title: title, start: start, end: end, id: id },
          success: function() {
            calendar.refetchEvents(); // Use calendar.refetchEvents
            alert('Event Update');
          }
        });
      },
      eventDrop: function(event) {
        var start = FullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
        var end = FullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");
        var title = event.title;
        var id = event.id;
        $.ajax({
          url: "/update",
          type: "POST",
          data: { title: title, start: start, end: end, id: id },
          success: function() {
            calendar.refetchEvents();
            alert("Event Updated");
          }
        });
      },
      eventClick: function(event) {
        if (confirm("Are you sure you want to remove it?")) {
          var id = event.id;
          $.ajax({
            url: "/ajax_delete",
            type: "POST",
            data: { id: id },
            success: function() {
              calendar.refetchEvents();
              alert("Event Removed");
            }
          });
        }
      },
    });
    calendar.render();
  });
  