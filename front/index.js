document.addEventListener('DOMContentLoaded', () => {
    // DOM 요소 가져오기
    const mainPage = document.getElementById('main-page');
    const reviewPage = document.getElementById('review-page');
    const goToReviewBtn = document.getElementById('go-to-review-btn');
    const goBackToMainBtn = document.getElementById('go-to-main-btn');
    const reviewForm = document.getElementById('review-form');
    const searchBtn = document.getElementById('search-btn');



    // 범용 별점 컴포넌트 초기화 함수
    function initRating(containerId, hiddenInputId, initial = 0) {
        const container = document.getElementById(containerId);
        const stars = container.querySelectorAll('.star');
        const hidden = document.getElementById(hiddenInputId);

        function update(value) {
            hidden.value = value;
            stars.forEach(star => {
                const v = parseInt(star.getAttribute('data-value'));
                if (v <= value) {
                    star.classList.add('checked');
                    star.style.color = 'gold';
                } else {
                    star.classList.remove('checked');
                    star.style.color = '#ccc';
                }
            });
        }

        stars.forEach(star => {
            star.addEventListener('click', function() {
                const v = parseInt(this.getAttribute('data-value'));
                update(v);
            });
            star.addEventListener('mouseover', function() {
                const v = parseInt(this.getAttribute('data-value'));
                stars.forEach(s => {
                    const sv = parseInt(s.getAttribute('data-value'));
                    s.style.color = sv <= v ? 'gold' : '#ccc';
                });
            });
            star.addEventListener('mouseout', function() {
                update(parseInt(hidden.value) || 0);
            });
        });

        update(initial);
    }

    // 초기화: 각 항목별로 실행
    initRating('pedal-rating', 'pedal-rating-value', 0);
    initRating('brake-rating', 'brake-rating-value', 0);
    initRating('tire-rating', 'tire-rating-value', 0);

    // 메인 페이지로 돌아가는 함수 (데이터 초기화 및 확인)
    function goToMainPage() {
        if (confirm('작성 중인 내용이 저장되지 않습니다. 메인 페이지로 돌아가시겠습니까?')) {
            reviewPage.style.display = 'none';
            mainPage.style.display = 'block';
            reviewForm.reset(); // 폼 내용 초기화
            // 별점 초기화
            document.getElementById('pedal-rating-value').value = 0;
            document.getElementById('brake-rating-value').value = 0;
            document.getElementById('tire-rating-value').value = 0;
            // 다시 렌더링
            initRating('pedal-rating', 'pedal-rating-value', 0);
            initRating('brake-rating', 'brake-rating-value', 0);
            initRating('tire-rating', 'tire-rating-value', 0);
        }
    }

    // 페이지 전환 기능 (메인 -> 리뷰)
    goToReviewBtn.addEventListener('click', () => {
        mainPage.style.display = 'none';
        reviewPage.style.display = 'block';
    });

    // 홈으로 돌아가기 버튼 클릭 이벤트
    goBackToMainBtn.addEventListener('click', goToMainPage);

    // 검색 버튼 클릭 이벤트
    searchBtn.addEventListener('click', () => {
        alert('검색 기능은 백엔드 구현이 필요합니다. UI 동작 확인!');
    });

    // 리뷰 제출 기능 (프론트엔드에서 데이터 수집 및 알림)
    reviewForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const bikeNumber = document.getElementById('bike-number').value.trim();
        const pedalRating = parseInt(document.getElementById('pedal-rating-value').value) || 0;
        const brakeRating = parseInt(document.getElementById('brake-rating-value').value) || 0;
        const tireRating = parseInt(document.getElementById('tire-rating-value').value) || 0;
        const reviewText = document.getElementById('review-text').value.trim();

        if (!bikeNumber || !reviewText) {
            alert('따릉이 번호와 리뷰 내용을 입력해 주세요.');
            return;
        }
        if (pedalRating <= 0 || brakeRating <= 0 || tireRating <= 0) {
            alert('모든 항목(페달링, 브레이크, 타이어)에 별점을 매겨 주세요.');
            return;
        }

        alert(`[리뷰 제출 완료 (UI 확인)]\n\n- 따릉이 번호: ${bikeNumber}\n- 페달링: ${pedalRating}점\n- 브레이크: ${brakeRating}점\n- 타이어: ${tireRating}점\n- 리뷰 내용: ${reviewText.substring(0, 60)}...\n\n실제 데이터 저장을 위해서는 백엔드 서버가 필요합니다.`);

        // 제출 후 메인 페이지로 복귀 (폼 내용 초기화 및 화면 전환)
        goToMainPage();
    });
});