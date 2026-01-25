async function loadPosts() {
  const res = await fetch("http://127.0.0.1:8000/forum");
  const posts = await res.json();
  const postsDiv = document.getElementById("posts");
  postsDiv.innerHTML = "";

  posts.forEach(post => {
    const div = document.createElement("div");
    div.className = "card";
    div.innerHTML = `
      <h3>${post.title}</h3>
      <p><strong>${post.user}</strong> - ${new Date(post.created_at).toLocaleString()}</p>
      <p>${post.content}</p>
    `;
    postsDiv.appendChild(div);
  });
}

document.getElementById("postForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const user = document.getElementById("user").value;
  const title = document.getElementById("title").value;
  const content = document.getElementById("content").value;

  await fetch("http://127.0.0.1:8000/forum", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user, title, content })
  });

  document.getElementById("postForm").reset();
  loadPosts();
});

loadPosts();