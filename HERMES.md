# Hướng dẫn sử dụng với Hermes

## Cài đặt

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
hermes profiles create trend

git clone https://github.com/Lucas-0911/trend-agent-webapp.git
cp trend-agent-webapp/skills/AGENT.md ~/.hermes/profiles/trend/
cp -r trend-agent-webapp/skills/trend-pipeline ~/.hermes/profiles/trend/skills/
cp trend-agent-webapp/skills/MEDIACRAWLER.md ~/.hermes/profiles/trend/skills/
```

## Chạy

```bash
hermes --profile trend
```

Nói: `tìm ngách` hoặc `chạy trend pipeline`

## Hermes sẽ làm
1. Thu thập (MediaCrawler hoặc hỏi từ khóa)
2. Đánh giá ngách — chỉ giữ cái đáng bán
3. Viết kịch bản video test 15–30s
4. Trả kết quả: ngách + kênh + kịch bản + việc làm ngay

## File skill
- skills/AGENT.md
- skills/trend-pipeline/SKILL.md
- skills/MEDIACRAWLER.md
