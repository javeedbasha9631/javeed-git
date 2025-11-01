// Simple JS to call API endpoints
const headersJSON = {'Content-Type': 'application/json'};

async function postJSON(path, body){
  const res = await fetch(path, {method: 'POST', headers: headersJSON, body: JSON.stringify(body)});
  return res.json();
}

document.getElementById('btn_register').addEventListener('click', async ()=>{
  const email = document.getElementById('reg_email').value || undefined;
  const mobile = document.getElementById('reg_mobile').value || undefined;
  const res = await postJSON('/register/', {email, mobile});
  document.getElementById('register_result').innerText = JSON.stringify(res);
});

document.getElementById('btn_login').addEventListener('click', async ()=>{
  const email = document.getElementById('login_email').value || undefined;
  const mobile = document.getElementById('login_mobile').value || undefined;
  const res = await postJSON('/login/', {email, mobile});
  document.getElementById('login_result').innerText = JSON.stringify(res);
});

document.getElementById('btn_verify').addEventListener('click', async ()=>{
  const email = document.getElementById('verify_email').value || undefined;
  const mobile = document.getElementById('verify_mobile').value || undefined;
  const code = document.getElementById('verify_code').value;
  const res = await postJSON('/verify-otp/', {email, mobile, code});
  document.getElementById('verify_result').innerText = JSON.stringify(res);
  if(res.access){
    // store access token
    localStorage.setItem('access_token', res.access);
    localStorage.setItem('refresh_token', res.refresh);
  }
});

document.getElementById('btn_profile').addEventListener('click', async ()=>{
  const token = localStorage.getItem('access_token');
  if(!token){
    document.getElementById('profile_result').innerText = 'No access token stored. Complete OTP verification first.';
    return;
  }
  const res = await fetch('/profile/', {method: 'GET', headers: {'Authorization': 'Bearer ' + token}});
  const data = await res.json();
  document.getElementById('profile_result').innerText = JSON.stringify(data);
});
