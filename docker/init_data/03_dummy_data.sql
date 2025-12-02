-- 개발/테스트 환경용 더미 데이터를 삽입합니다.
-- 1. users 테이블 더미 데이터 삽입
INSERT INTO users (email, password, name, nickname, phone_number, is_superuser, is_active, last_login, created_at, updated_at) VALUES
('chulsoo@example.com', 'hashed_pw_1', '김철수', 'chulsoo_dev', '010-1111-2222', FALSE, TRUE, NOW(), NOW(), NOW()),
('younghee@example.com', 'hashed_pw_2', '이영희', 'younghee_dev', '010-3333-4444', FALSE, TRUE, NOW(), NOW(), NOW()),
('minjun@example.com', 'hashed_pw_3', '박민준', 'minjun_dev', '010-5555-6666', FALSE, TRUE, NULL, NOW(), NOW());

-- 2. accounts 테이블 더미 데이터 삽입
-- (user_id는 위 users 테이블의 ID를 순서대로 1, 2, 3으로 가정)
INSERT INTO accounts (user_id, account_number, bank_code, account_type, name, created_at) VALUES
-- 김철수 (ID: 1) 계좌
(1, '004-921345678', '004', 'CHECKING', '철수 주거래 입출금', NOW()),
-- 이영희 (ID: 2) 계좌
(2, '088-100298765', '088', 'CHECKING', '영희 생활비 통장', NOW()),
-- 김철수 (ID: 1) 적금 계좌
(1, '020-567812340', '020', 'SAVING', '철수 목표 달성 적금', NOW()),
-- 박민준 (ID: 3) 주식 계좌
(3, '264-001998877', '264', 'STOCK', '민준 투자 주식계좌', NOW());

-- 3. transactions 테이블 더미 데이터 삽입
-- (account_id는 위 accounts 테이블의 ID를 순서대로 1, 2, 3, 4로 가정)
INSERT INTO transactions (account_id, transaction_type, transaction_method, amount, transaction_details, transaction_timestamp) VALUES
-- 계좌 ID: 1 (철수 주거래)
(1, 'DEPOSIT', 'TRANSFER', 5000000, '급여 입금', '2025-11-01 09:00:00'),
(1, 'WITHDRAW', 'CARD', 150000, '온라인 쇼핑몰 결제', '2025-11-05 18:30:00'),
(1, 'WITHDRAW', 'ATM', 50000, '현금 인출', '2025-11-10 11:00:00'),

-- 계좌 ID: 2 (영희 생활비)
(2, 'DEPOSIT', 'TRANSFER', 2500000, '용돈 입금', '2025-11-01 10:00:00'),
(2, 'WITHDRAW', 'AUTOMATIC_TRANSFER', 700000, '월세 자동이체', '2025-11-05 00:00:00'),

-- 계좌 ID: 3 (철수 적금)
(3, 'DEPOSIT', 'AUTOMATIC_TRANSFER', 500000, '자동 적금 이체', '2025-11-15 09:00:00'),

-- 계좌 ID: 4 (민준 투자)
(4, 'DEPOSIT', 'TRANSFER', 10000000, '시드머니 입금', '2025-11-20 15:00:00');