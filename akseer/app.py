from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ===================== IMAGE SETTINGS ===================== #
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ===================== PROFILE DATA ===================== #
profile = {
    "name": "Mohammed Akseer",
    "bio": "AI & Flask learner building modern websites and applications with passion and consistency.",
    "age": 18,
    "location": "Chennai, India",
    "profile_img": "uploads/profile.jpg"
}
    
skills = ["Python", "Flask", "HTML", "CSS", "JavaScript", "Bootstrap"]
hobbies = ["Coding", "Gaming", "Learning New Tech", "Productivity"]

education = [
    {"degree": "B.Tech. AI & DS", "college": "Velammal Engineering College", "year": "2024–2028"},
    {"degree": "High School", "school": "Oriental Arabic School", "year": "2022–2024"}
]

projects = [
    {
        "id": 1,
        "title": "Optical Store Management Website",
        "description": "Inventory + billing + customer tracking system.",
        "image": "uploads/project1.jpg"
    },
    {
        "id": 2,
        "title": "Flask Portfolio & Blog System",
        "description": "Dynamic website with blogs + profile upload features.",
        "image": "uploads/project2.jpg"
    }
]

contact = {
    "email": "akseer@example.com",
    "phone": "6382168341",
    "instagram": "@its_me_Akseer_07",
    "location": "Chennai, India"
}

# ===================== BLOG DATA ===================== #
blogs = [
    {
        "id": 1,
        "title": "Getting Started with Flask",
        "content": "This blog explains Flask basics such as routing, templates, and folder structure.",
        "date": "2025-02-10"
    },
    {
        "id": 2,
        "title": "Why I Love Python",
        "content": "Python is simple, readable, and powerful for backend, AI, and automation.",
        "date": "2025-02-15"
    }
]


# ===================== ROUTES ===================== #
@app.route("/")
def home():
    return render_template(
        "index.html",
        profile=profile,
        skills=skills,
        hobbies=hobbies,
        education=education,
        projects=projects
    )

@app.route("/about")
def about():
    return render_template(
        "about.html",
        profile=profile,
        skills=skills,
        education=education,
        contact=contact
    )



@app.route("/blogs")
def blogs_page():
    return render_template("blogs.html", blogs=blogs)


@app.route("/blog/<int:id>")
def blog_detail(id):
    post = next((b for b in blogs if b["id"] == id), None)
    if not post:
        return "Blog not found", 404
    return render_template("blog_detail.html", post=post)
 
@app.route("/add-blog", methods=["GET", "POST"])
def add_blog():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        blogs.append({
            "id": len(blogs) + 1,
            "title": title,
            "content": content,
            "date": "2025-02-20",
            "image": None
        })

        return redirect(url_for("blogs_page"))

    return render_template("add_blog.html")



# ===================== PROJECT IMAGE UPLOAD (OPTIONAL) ===================== #
@app.route("/upload-project/<int:id>", methods=["POST"])
def upload_project(id):
    file = request.files.get("project_image")

    if file and allowed_file(file.filename):
        filename = secure_filename(f"project{id}.jpg")
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        project = next((p for p in projects if p["id"] == id), None)
        if project:
            project["image"] = f"uploads/{filename}"

    return redirect(url_for("home"))


# ===================== RUN ===================== #
if __name__ == "__main__":
    app.run()
    app.run(host="0.0.0.0", port=5000, debug=True)
