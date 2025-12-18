# 1. Node.js 18 (과제 요구 버전)
FROM node:18-alpine

# 2. 컨테이너 내부 작업 디렉토리
WORKDIR /app

# 3. 의존성 파일만 먼저 복사 (캐시 최적화)
COPY package*.json ./

# 4. 프로덕션 의존성만 설치
RUN npm install --production

# 5. 나머지 소스코드 복사
COPY . .

# 6. Node 서버 포트
EXPOSE 3000

# 7. 애플리케이션 실행
CMD ["npm", "start"]
