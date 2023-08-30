function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addFavoriteListener(elementId, url, productId) {
    document.getElementById(elementId).addEventListener('click', function() {
        const csrftoken = getCookie('csrftoken');
        var formData = new FormData();
        formData.append('product_id', productId);
        formData.append('csrfmiddlewaretoken', csrftoken);
    
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        })
        .then(response => {
            if (response.status === 200) {
                return " filled";
            } else if (response.status === 204) {
                return "";
            } else {
                throw new Error('Request failed with status ' + response.status);
            }
        })
        .then(data => {
            document.getElementById(elementId).className = "favorite" + data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}
    