export async function login(values): Promise<{access_token: string, token_type: string} | null> {
  const authentication_creds = new URLSearchParams({
    username: values.username,
    password: values.password,
  });

  try {
    // env var BACKEND_SERVER_URL
    const backend_url = process.env.BACKEND_SERVER_URL;
    const response = await fetch(`${backend_url}/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: authentication_creds.toString(),  // URL-encoded form data
    });

    // Check if the response is OK (status code 200-299)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    // Handle errors gracefully
    console.error('Error:', error);
  }
  return null;
}