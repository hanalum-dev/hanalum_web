<template>
  <div>
    <form-wizard
      title="논문 리뷰 신청하기"
      subtitle="연구 계획서와 논문 초안을 등록하고 분야에 맞는 졸업생 리뷰어에게 리뷰를 받아보세요!"
      next-button-text="다음"
      back-button-text="이전"
      finish-button-text="제출"
      color="#6f83e7"
      error-color="#ff5f5f"
      shape="circle"
      @on-complete="completeHandler">
      <tab-content title="기본 정보">
        <b-card class="p-5 m-5">
          <h5 class="mb-5">논문의 기본 정보를 입력해주세요.</h5>
          <b-form-group
            class="m-3"
            label="논문 제목"
            label-for="input-paper-title">
            <b-form-input
              name="paper-title"
              id="input-paper-title"
              v-model="form.paperTitle"
              placeholder="논문 제목을 작성해주세요."
            />
          </b-form-group>
          <b-form-group
            class="m-3"
            label="논문 부제목"
            label-for="input-paper-subtitle">
            <b-form-input
              name="paper-subtitle"
              id="input-paper-subtitle"
              v-model="form.paperSubtitle"
              placeholder="논문 부제목을 작성해주세요."
            />
          </b-form-group>
          <b-form-group
            class="m-3"
            label="논문 요약"
            label-for="input-paper-summary">
            <b-form-textarea
              name="paper-summary"
              id="input-paper-summary"
              v-model="form.paperSummary"
              placeholder="논문 요약을 작성해주세요."
            />
          </b-form-group>
        </b-card>
      </tab-content>
      <tab-content title="파일 제출">
        <b-card class="p-5 m-5">
          <h5 class="mb-5">논문 파일을 제출해주세요.</h5>
          <b-form-group
            class="m-3"
            label="논문 파일"
            label-for="input-paper-file">
            <b-form-file
              name="paper-file"
              id="input-paper-file"
              v-model="form.paperFile"
              :state="Boolean(form.paperFile)"
              placeholder="논문 파일을 업로드해주세요."
              drop-placeholder="논문 파일을 여기에 드래그 앤 드랍해주세요."
            />
          </b-form-group>
        </b-card>
      </tab-content>
      <tab-content title="추가 정보">
        <b-card class="p-5 m-5">
          <h5 class="mb-5">리뷰어에게 남기고 싶은 말이 있으신가요?</h5>
          <b-form-group
            class="m-3"
            label="리뷰어에게 요청합니다!"
            label-for="input-paper-comment">
            <b-form-textarea
              name="paper-comment"
              id="input-paper-comment"
              v-model="form.paperComment"
            />
          </b-form-group>
        </b-card>
      </tab-content>
    </form-wizard>
    <input ref="submit" type="submit" hidden>
  </div>
</template>

<script>
import { FormWizard, TabContent } from 'vue-form-wizard';

export default {
  name: 'JohaApplyFormWizard',
  props: {
    msg: String
  },
  data() {
    return {
      form: {
        paperTitle: '',
        paperSubTitle: '',
        paperSummary: '',
        paperFile: null,
        paperComment: '',
      }
    }
  },
  components: {
    FormWizard,
    TabContent
  },
  methods: {
    completeHandler(){
      this.$refs.submit.click();
    },
  }
}
</script>
