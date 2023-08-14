const searchField = document.querySelector("#searchField");
const paginationContainer = document.querySelector(".pagination-container");
const doc_title = document.title
const task_count = document.getElementById("task_count");
let task_count_initial = task_count.innerHTML;
const tbody = document.querySelector("#table-body-data");
let task_list = tbody.innerHTML;
const no_results = document.getElementById("no-results");

searchField.addEventListener("keyup", (e) => {
  const delay = setTimeout(() => {
    searchFunction(e);
  }, 500);
  return () => clearTimeout(delay);
});

const searchFunction = (e) => {
  const searchValue = e.target.value;
  no_results.style.display = "none";
  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = "";
    if (doc_title == "Tasks")
    {
      fetch("/smart-over/search", {
        body: JSON.stringify({ search_query: searchValue }),
        method: "POST",
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          task_count.innerHTML = data.length;
          if (data.length === 0) {
            no_results.style.display = "block";
          } else {
            no_results.style.display = "none";
            tbody.innerHTML = "";
            data.forEach((item) => {
              let priority;
              if (item.priority == 1){
                priority = "Low"
              }
              else if (item.priority == 2){
                priority = "Medium"
              }
              else if (item.priority == 3){
                priority = "High"
              }
              else{
                priority = "Critical"
              }
  
              tbody.innerHTML += `
                  <tr>
                  <td>${
                    item.description.length > 30
                      ? item.description.substring(0, 29) + "..."
                      : item.description
                  }</td>
                  <td>${
                    item.created_by__username}</td>
                    <td>${priority}</td>
                    <td>${item.date}</td>
                    <td>
                    <div class="dropdown ms-auto">
                    <i class="fas fa-ellipsis-vertical" data-bs-toggle="dropdown" aria-expanded="false"></i>
                    <ul class="dropdown-menu">
                      <li>
                        <a href="/smart-over/view-task/${item.id}" >
                          <span class="dropdown-item">
                            <i class="fas fa-pen mx-2"></i> View
                          </span>
                        </a>
                      </li>
                      <li>
                        <a href="/smart-over/close-task/${item.id}">                                      
                          <span class="dropdown-item">
                              <i class="fas fa-print mx-2"></i> Close Task
                          </span>
                        </a>
                      </li>
                    </ul>
                  </div>
                  </td>
                  </tr>`;
            });
          }
        });
    }
    else{

      fetch("/smart-over/search-closed", {
        body: JSON.stringify({ search_query: searchValue }),
        method: "POST",
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          task_count.innerHTML = data.length;
          if (data.length === 0) {
            no_results.style.display = "block";
          } else {
            no_results.style.display = "none";
            tbody.innerHTML = "";
            data.forEach((item) => {
              let priority;
              if (item.priority == 1){
                priority = "Low"
              }
              else if (item.priority == 2){
                priority = "Medium"
              }
              else if (item.priority == 3){
                priority = "High"
              }
              else{
                priority = "Critical"
              }
  
              tbody.innerHTML += `
              <tr>
              <td>${
                item.description.length > 30
                  ? item.description.substring(0, 29) + "..."
                  : item.description
              }</td>
              <td>${
                item.created_by__username}</td>
                <td>${priority}</td>
                <td>${item.date}</td>
                <td>${item.closing_date}</td>
                <td>${item.closed_by__username}</td>
                <td>${item.remarks}</td>
                <td>
                <div class="dropdown ms-auto">
                <i class="fas fa-ellipsis-vertical" data-bs-toggle="dropdown" aria-expanded="false"></i>
                <ul class="dropdown-menu">
                  <li>
                    <a href="/smart-over/view-task/${item.id}" >
                      <span class="dropdown-item">
                        <i class="fas fa-pen mx-2"></i> View
                      </span>
                    </a>
                  </li>
                  <li>
                    <a href="/smart-over/delete-task/${item.id}">                                      
                      <span class="dropdown-item">
                          <i class="fas fa-trash mx-2"></i> delete
                      </span>
                    </a>
                  </li>
                </ul>
              </div>
              </td>
              </tr>`;
            });
          }
        });

    }

  } else {
    paginationContainer.style.display = "block";
    tbody.innerHTML = task_list;
    task_count.innerHTML = task_count_initial;
  }
};

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
