<script setup>
import getPaymentLink from '@api/order'
</script>

<template>
    <form v-on:submit.prevent.stop="getOrder()">

        <div class="field">
            <label class="label">Codigo de Estacionamiento</label>
            <div class="control">
                <input class="input" type="text" placeholder="Text input" name="orderCode" id="orderCode" v-model="orderCode">
            </div>
        </div>

        <div class="field">
            <div class="control">
                <label class="checkbox">
                    <input type="checkbox">
                    I agree to the <a href="#">terms and conditions</a>
                </label>
            </div>
        </div>

        <div class="field is-grouped">
            <div class="control">
                <button class="button is-link">Pagar</button>
            </div>
            <div class="control">
                <a href="/">
                    <button class="button is-text">Salir</button>
                </a>
            </div>
        </div>
    </form>
</template>

<script>
export default {
    data() {
        return {
            orderCode: "",
        };
    },
    methods: {
        async getOrder() {
            const link = await getPaymentLink(this.orderCode)
            if (link != null){
                window.location.replace(String(link.link))
            }
            return
        }
    }
}
</script>