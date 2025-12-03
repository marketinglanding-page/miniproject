-- =======================================================
-- 1. 사용자 데이터 (users 테이블)
-- =======================================================
INSERT INTO users (
    id, email, name, nickname, password, is_superuser, is_staff, is_active,
    date_joined, last_login, created_at, updated_at
) VALUES
-- User 1: 철수
(1, 'chulsoo@test.com', '철수', '쿨가이철수', 'sha256$test_hash_chulsoo', TRUE, TRUE, TRUE,
 NOW(), NOW(), NOW(), NOW()),

-- User 2: 영희
(2, 'younghee@test.com', '영희', '퀸영희', 'sha256$test_hash_younghee', FALSE, FALSE, TRUE,
 NOW(), NOW(), NOW(), NOW()),

-- User 3: 민준
(3, 'minjun@test.com', '민준', '투자왕민준', 'sha256$test_hash_minjun', FALSE, FALSE, TRUE,
 NOW(), NOW(), NOW(), NOW());

-- 시퀀스 업데이트 (새로 삽입된 id 값 이후부터 시작하도록 설정)
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

-- =======================================================
-- 2. 계좌 데이터 (accounts 테이블)
-- =======================================================
INSERT INTO accounts (
    id, user_id, account_number, bank_code, account_type, name, created_at
) VALUES
-- User 1 (철수) 계좌
(1, 1, '110-123456-78', '088', 'CHECKING', '철수 주거래 통장', NOW()),
(3, 1, '110-555555-11', '088', 'SAVING', '철수 적금', NOW()),

-- User 2 (영희) 계좌
(2, 2, '220-987654-32', '004', 'SAVING', '영희 생활비 계좌', NOW()),

-- User 3 (민준) 계좌
(4, 3, '330-111222-33', '090', 'INVESTMENT', '민준 투자 계좌', NOW());

-- 시퀀스 업데이트
SELECT setval('accounts_id_seq', (SELECT MAX(id) FROM accounts));

-- =======================================================
-- 3. 거래 내역 데이터 (transactions 테이블)
--    balance_after는 각 계좌의 초기 잔액 0원 가정하에 순차적으로 계산됨.
-- =======================================================

INSERT INTO transactions (
    account_id, transaction_type, transaction_method, amount,
    transaction_details, transaction_timestamp, balance_after,
    created_at, updated_at
) VALUES
-- 계좌 ID: 1 (철수 주거래)
-- 1. 급여 입금 (잔액: 5,000,000)
(1, 'INCOME', 'BANK_TRANSFER', 5000000, '급여 입금', '2025-11-01 09:00:00', 5000000, NOW(), NOW()),
-- 2. 온라인 쇼핑몰 결제 (잔액: 4,850,000)
(1, 'EXPENSE', 'CARD_PAYMENT', 150000, '온라인 쇼핑몰 결제', '2025-11-05 18:30:00', 4850000, NOW(), NOW()),
-- 3. 현금 인출 (잔액: 4,800,000)
(1, 'EXPENSE', 'CASH', 50000, '현금 인출', '2025-11-10 11:00:00', 4800000, NOW(), NOW()),

-- 계좌 ID: 2 (영희 생활비)
-- 1. 용돈 입금 (잔액: 2,500,000)
(2, 'INCOME', 'BANK_TRANSFER', 2500000, '용돈 입금', '2025-11-01 10:00:00', 2500000, NOW(), NOW()),
-- 2. 월세 자동이체 (잔액: 1,800,000)
(2, 'EXPENSE', 'BANK_TRANSFER', 700000, '월세 자동이체', '2025-11-05 00:00:00', 1800000, NOW(), NOW()),

-- 계좌 ID: 3 (철수 적금)
-- 1. 자동 적금 이체 (잔액: 500,000)
(3, 'INCOME', 'BANK_TRANSFER', 500000, '자동 적금 이체', '2025-11-15 09:00:00', 500000, NOW(), NOW()),

-- 계좌 ID: 4 (민준 투자)
-- 1. 시드머니 입금 (잔액: 10,000,000)
(4, 'INCOME', 'BANK_TRANSFER', 10000000, '시드머니 입금', '2025-11-20 15:00:00', 10000000, NOW(), NOW());

-- 시퀀스 업데이트
SELECT setval('transactions_id_seq', (SELECT MAX(id) FROM transactions));