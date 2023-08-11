<template>
<div>
  <!-- <b-jumbotron>
    <template v-slot:header>Michigan Imputation Server</template>

    <template v-slot:lead>
     Free Next-Generation Genotype Imputation Service
    </template>

    <b-button variant="primary" href="#">Sign up now</b-button>
    <b-button variant="success" href="#">Login</b-button>
  </b-jumbotron> -->
  <div id="content" class="" style="margin-top: 3rem;">
    <div class="fullsize-container">
      <div class="jumbotron jumbotron-fluid text-white text-center" style="background: #4f5d73; margin-bottom: 0px; ">
        <div class="container">
          <h1 class="jumbotron-heading">Imputation Server</h1>
          <p class="lead text-center">
            Free Next-Generation Genotype Imputation Service 
          </p> 
            <p >
              <br>
              <router-link v-if="loggedIn" class="btn btn-lg btn-success"  to="/register">Sign up now</router-link>&nbsp;
              <router-link v-if="loggedIn" class="btn btn-lg btn-outline-light" to="/login">Login</router-link>
            </p>
        </div>
      </div>

      <!-- dark:  #303846 -->
      <!-- light: #71829d -->
      <div class="text-white" style="background: #71829d;">
        <div class="container pt-3">
          <div class="row justify-content-center text-center ">
            <div class="col-md-3 text-center">
              <p>
                <span class="lead" style="font-size: 200%;">96.1M</span><br>Imputed Genomes
              </p>
            </div>
            <div class="col-md-3 text-center">
              <p>
                <span class="lead" style="font-size: 200%;">9726</span><br>Registered Users
              </p>
            </div>
            <div class="col-md-3 text-center">
              <p>
                <span class="lead" style="font-size: 200%;">6</span><br>Running Jobs
              </p>
            </div>
          </div>
        </div>
      </div>


      <!-- News and Logos -->
      <div class="py-5 bg-light">
        <div class="container  ">
          <div class="card ">
            <div class="card-body">
              <div class="container">
                <div class="row">
                  <div class="col-md-8">
                    <h5 style="padding-top: 10px; padding-bottom: 0px; margin-bottom: 10px;">Latest News</h5>
                    <hr style="padding-top: 0px; margin-top: 0px;">
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 21 May 2021</small>
                      We have increased the max sample size to 110k.                                                           
                    </p>
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 15 April 2021</small>
                      Update to new framework completed! Currently, max sample size will be limited to 25k, but we expect to lift this limitation in the next few weeks.                                                              
                    </p> 
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 18 March 2020</small>
                      Due to coronavirus-related impacts support may be slower than usual. If you haven't heard back from us after a week or so, feel free to e-mail again to check on the status of things. Take care!            
                    </p>
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 07 November 2019</small><br>
                      Updated MIS to v1.2.4! Major improvements: Minimac4 for imputation, improved chrX support, QC check right after upload, better documentation. Checkout out our <a href="https://github.com/genepi/imputationserver" target="_blank">GitHub repository</a> for further information. 
                    </p> 
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 17 October 2019</small><br>
                      Michigan Imputation Server @ ASHG19. All information is available <a href="https://imputationserver.sph.umich.edu/ashg19/" target="_blank">here</a>.
                    </p>
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 27 November 2018</small><br>
                      Redesigned user interface to improve user experience.
                    </p>
                                                              
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 27 June 2017</small><br>
                      Updated pipeline to v1.0.2. Release notes can be found <a href="https://github.com/genepi/imputationserver/releases/tag/1.0.2" target="_blank">here</a>.
                    </p>
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 29 Aug 2016</small><br>
                      Imputation server paper is out now: <a href="http://www.nature.com/ng/journal/v48/n10/full/ng.3656.html" target="_blank">Das et al., Nature Genetics 2016</a>
                    </p>
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 14 June 2016</small><br>
                      Supporting <a target="_blank" href="https://github.com/seppinho/23andme-tools.git">23andMe input format</a>.
                    </p>
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 19 April 2016</small><br>
                      Updated <a target="_blank" href="http://www.haplotype-reference-consortium.org/">HRC Panel (r1.1)</a> available.
                    </p>
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 12 January 2016</small><br>
                      New Reference Panel (<a target="_blank" href="/#!pages/caapa">CAAPA</a>) available.
                    </p>
                    <p>
                      <small class="text-muted"><i class="far fa-calendar-alt"></i> 24 April 2015</small><br>
                      <a target="_blank" href="http://www.haplotype-reference-consortium.org/">HRC release 1</a> (64,976 haplotypes at 39,235,157 SNPs) is now ready for use for HRC consortium members.
                    </p>

                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-light py-5" style="margin-top: 0px;">
        <div class="container  ">
          <h2 class="text-center pb-5">The <b><u>easiest</u></b> way to impute genotypes</h2>
          <!-- Workflow Description -->
          <div class="card-deck text-center ">
            <div class="card box-shadow">
              <div class="card-body">
                <p><img :src="url.up" width="105px"></p>
                <b>Upload your genotypes</b> to our server located in Michigan.<br> All interactions with the server are <b>secured</b>.
              </div>
            </div>
            <div class="card box-shadow">
              <div class="card-body">
                <p><img :src="url.impute" width="105px"></p>
                <b>Choose a reference panel</b>. We will take care of pre-phasing and imputation.
              </div>
            </div>
            <div class="card box-shadow">
              <div class="card-body">
                <p><img :src="url.down" width="105px"></p>
                <b>Download the results</b>.<br>All results are encrypted with a one-time password. After 7 days, all results are deleted from our server.
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="py-5 bg-light">
        <div class="container">
          <h2 class="text-center pb-5 ">Wide-range of reference panels supported</h2>
          <div class="card-deck  text-center ">
            <div class="card " style="border-top-color: #76c2af; border-top-width: 5px;">
              <div class="card-body">
                HapMap<br>Release 2
              </div>
            </div>
            <div class="card " style="border-top-color: #e0995e; border-top-width: 5px;">
              <div class="card-body">
                1000 Genomes<br>Phase 1
              </div>
            </div>
            <div class="card " style="border-top-color: #4f5d73; border-top-width: 5px;">
              <div class="card-body">
                1000 Genomes<br>Phase 3
              </div>
            </div>
            <div class="card " style="border-top-color: #4f5d73; border-top-width: 5px;">
              <div class="card-body">
                CAAPA<br>African American
              </div>
            </div>
            <div class="card " style="border-top-color: #4f5d73; border-top-width: 5px;">
              <div class="card-body">
                Haplotype Reference<br>Consortium
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</div>
</template>

<script>
import doCookie from "@/utils/cookie"

export default {
    name:"home",
  created() {
    // Check if the "imputation-username" cookie exists
    this.loggedIn = this.checkCookie("imputation-username");
  },
    data () {
      return {
        url:{
          impute:"./image/impute.png",
          down:"./image/down-cloud.png",
          up:"./image/up-cloud.png"
        
        },
        loggedIn: false,
      }
    },
    methods: {
    checkCookie(cookieName) {
      
      const imputation_username = doCookie.getCookie(cookieName)
      this.imputation_username = imputation_username
      if ( imputation_username.length === 0) {
        return true; // Cookie exists, set loggedIn to true
      }
      
      return false; // Cookie doesn't exist, set loggedIn to false
    },
  },
    mounted () {
      
    }
}
</script>

<style  scoped>

.jumbotron {
    padding: 4rem 2rem;
}
</style>