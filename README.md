# Trend Agent WebApp

MediaCrawler → chấm điểm (Jev API hoặc **laya-mlx local**) → lưu DB → phân tích.

## Cài đặt

```bash
git clone https://github.com/Lucas-0911/trend-agent-webapp.git
cd trend-agent-webapp
pip install -r requirements.txt
```

### Trên MacBook M1/M2/M3 (Apple Silicon) — dùng laya-mlx local

```bash
pip install laya-mlx
export USE_LAYA_MLX=true
```

Lần đầu sẽ tải model (~1GB). Sau đó chạy hoàn toàn local, không cần API key Jev.

## Chạy

```bash
export MEDIACRAWLER_PATH=~/MediaCrawler
export TYPESAFE_API_KEY=your_key          # nếu dùng Jev
export USE_LAYA_MLX=true                  # nếu dùng laya-mlx trên Mac

uvicorn app:app --host 0.0.0.0 --port 8000
```

Mở: **http://localhost:8000**

## Ghi chú

- `laya-mlx` chỉ chạy trên Apple Silicon (M1+), macOS 14+, Python 3.11+.
- MediaCrawler: https://github.com/NanmiCoder/MediaCrawler
