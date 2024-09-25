async function login() {
  const authentication_creds = new URLSearchParams({
    username: '',
    password: '',
  });

  try {
    const response = await fetch('http://localhost:8080/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: authentication_creds.toString(),  // URL-encoded form data
    });

    // Check if the response is OK (status code 200-299)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log(data); // This will log the parsed JSON response
  } catch (error) {
    // Handle errors gracefully
    console.error('Error:', error);
  }
}


export default async function Home() {
  await login();

  return (
    <main>
      heyo
    </main>
  );
}
