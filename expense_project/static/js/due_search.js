// For page total
ele = document.getElementById("page-total")
total = parseFloat(ele.innerHTML).toFixed(2)
ele.innerHTML = total
const doc_title = document.title
const searchField = document.querySelector("#searchField");
const paginationContainer = document.querySelector(".pagination-container");
const dues_count = document.getElementById("dues_count");
let due_count_initial = dues_count.innerHTML;
const tbody = document.querySelector("#table-body-data");
let due_list = tbody.innerHTML;
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
    console.log("Items fetched");
    fetch("/due/search", {
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
        dues_count.innerHTML = data.length;
        if (data.length === 0) {
            no_results.style.display = "block";
        } else {
            no_results.style.display = "none";
            tbody.innerHTML = "";
            if (doc_title == "Dues"){
                data.forEach((item) => {
                    console.log(item.received_at)
                    if (item.received_at != null) {
                        tbody.innerHTML += `
                        <tr>
                        <td>${item.amount}</td>
                        <td>${item.source__source__source}</td>
                        <td>${
                            item.description.length > 30
                            ? item.description.substring(0, 29) + "..."
                            : item.description
                        }</td>
                        <td>${item.created_at}</td>
                        <td>${item.source__created_by}</td>
                        <td>${item.received_at}</td>
                        <td>
                            <div class="dropdown ms-auto">
                            <i class="fas fa-ellipsis-vertical" data-bs-toggle="dropdown" aria-expanded="false"></i>
                            <ul class="dropdown-menu">
                                <li>
                                <a href="/due/delete-due/${item.id}">
                                    <span class="dropdown-item">
                                    <i class="fas fa-trash mx-2"></i> Delete
                                    </span>
                                </a>
                                </li>
                            </ul>
                            </div>
                        </td>
                        </tr>`;
                    }
                    else{
                        tbody.innerHTML += `
                        <tr>
                        <td>${item.amount}</td>
                        <td>${item.source__source__source}</td>
                        <td>${
                            item.description.length > 30
                            ? item.description.substring(0, 29) + "..."
                            : item.description
                        }</td>
                        <td>${item.created_at}</td>
                        <td>${item.source__created_by}</td>
                        <td>${item.received_at}</td>
    
                        <td>
                        <div class="dropdown ms-auto">
                        <i class="fas fa-ellipsis-vertical" data-bs-toggle="dropdown" aria-expanded="false"></i>
                        <ul class="dropdown-menu">
                            <li>
                            <a href="/due/edit-due/${item.id}" >
                                <span class="dropdown-item">
                                <i class="fas fa-pen mx-2"></i> Edit
                                </span>
                            </a>
                            </li>
                            <li>
                            <a href="/due/due-received/${item.id}">                                      
                                <span class="dropdown-item">
                                <i class="fas fa-money-bill"></i> Received
                                </span>
                            </a>
                            </li>
                        </ul>
                        </div>
                        </td>
                        </tr>`;
                    }
                });
            }
            else{
                data.forEach((item) => {
                    console.log(item.received_at)
                    if (item.received_at != null) {
                        tbody.innerHTML += `
                        <tr>
                        <td>${item.amount}</td>
                        <td>${item.source__source__source}</td>
                        <td>${
                            item.description.length > 30
                            ? item.description.substring(0, 29) + "..."
                            : item.description
                        }</td>
                        <td>${item.created_at}</td>
                        <td>${item.source__created_by}</td>
                        <td>${item.received_at}</td>
    
                        <td>
                            <div class="dropdown ms-auto">
                            <i class="fas fa-ellipsis-vertical" data-bs-toggle="dropdown" aria-expanded="false"></i>
                            <ul class="dropdown-menu">
                                <li>
                                <a href="/due/view-due/${item.id}">
                                    <span class="dropdown-item">
                                    <i class="fas fa-eye"></i> View
                                    </span>
                                </a>
                                </li>
                            </ul>
                            </div>
                        </td>
                        </tr>`;
                    }
                    else{
                        tbody.innerHTML += `
                        <tr>
                        <td>${item.amount}</td>
                        <td>${item.source__source__source}</td>
                        <td>${
                            item.description.length > 30
                            ? item.description.substring(0, 29) + "..."
                            : item.description
                        }</td>
                        <td>${item.created_at}</td>
                        <td>${item.source__created_by}</td>
                        <td>${item.received_at}</td>
    
                        <td>
                        <div class="dropdown ms-auto">
                        <i class="fas fa-ellipsis-vertical" data-bs-toggle="dropdown" aria-expanded="false"></i>
                        <ul class="dropdown-menu">
                            <a href="/due/due-received/${item.id}">                                      
                                <span class="dropdown-item">
                                <i class="fas fa-money-bill"></i> Received
                                </span>
                            </a>
                            </li>
                        </ul>
                        </div>
                        </td>
                        </tr>`;
                    }
                });
            }
        }
        });
    } else {
    paginationContainer.style.display = "block";
    tbody.innerHTML = due_list;
    dues_count.innerHTML = due_count_initial;
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