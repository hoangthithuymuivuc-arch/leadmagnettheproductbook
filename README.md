# The Product Book (bản tóm tắt)

Site tĩnh HTML: bìa, mục lục, các chương tách file, tải nội dung qua `fetch` (hoặc iframe khi mở file local).

## Xem trên máy

Trong thư mục này, chạy một máy chủ tĩnh rồi mở trình duyệt (không nên mở trực tiếp `file://` vì trình duyệt có thể chặn tải chương).

```bash
python -m http.server 8080
```

Sau đó mở: `http://127.0.0.1:8080/` hoặc `http://127.0.0.1:8080/Book.html`.

## Đẩy lên GitHub

1. Tạo repository mới trên GitHub (có thể để public hoặc private).
2. Trong thư mục dự án:

```bash
git init
git add .
git commit -m "Initial publish: The Product Book (HTML)"
git branch -M main
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

Thay `<user>` và `<repo>` bằng tài khoản và tên repo của bạn.

## GitHub Pages

1. Repo trên GitHub → **Settings** → **Pages**.
2. **Build and deployment**: nguồn **Deploy from a branch**, branch **main**, thư mục **/ (root)**.
3. Lưu. Sau vài phút site có dạng `https://<user>.github.io/<repo>/` — file `index.html` sẽ chuyển sang `Book.html`.

File `.nojekyll` giúp GitHub không chạy Jekyll lên các file HTML/CSS tĩnh.

## PDF (tùy chọn)

Cần Python, `beautifulsoup4`, `playwright` và Chromium (`playwright install chromium`). Chạy:

```bash
python build_book_pdf.py
```

File PDF sinh ra được liệt kê trong `.gitignore`; nếu muốn đưa PDF lên repo, xóa dòng tương ứng trong `.gitignore` rồi `git add` file PDF.

## Vercel

Đã có `vercel.json` (redirect `/` → `/Book.html`). Kết nối repo với Vercel như project static thông thường.
