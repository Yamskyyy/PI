function sign_out() {
    $.removeCookie("mytoken", { path: "/" });
    alert("Signed out!");
    window.location.href = "/login";
}