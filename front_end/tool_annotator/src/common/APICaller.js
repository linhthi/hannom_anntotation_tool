import axios from "axios";

export function postAPI(strAPI, data, callback) {
    axios({
        method: "post",
        url: strAPI,
        data: data,
        headers: {
            "Content-Type": "application/json"
        }
    }).then(data => {
        callback(data)
    }).catch(function (error) {

    });
}

export function getAPI(strAPI, callback) {
    axios.defaults.headers["Content-Type"] =
        "application/x-www-form-urlencoded";

    axios.get(strAPI).then(_res => {
        callback(_res);
    })
        .catch(function (error) {
            console.log(error);
            callback([]);
        });

}